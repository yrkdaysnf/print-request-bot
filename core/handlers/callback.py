import asyncio, os
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from core.keyboards.inline import pay_inline, cancel, cancelorprint, canceldelete, cancelordelete, statuschange, delete
from core.data.sql import create_file, create_user, get_balance, edit_user_balance, get_fileinfo, delete_file, edit_file_status, get_username, get_all_files_in_status
from core.util.statesform import Comment


async def get_comment(message: Message, bot:Bot, state: FSMContext):
    await state.update_data(comment=message.text)
    messageid = await state.get_data()
    await bot.edit_message_caption(message.from_user.id, messageid.get('messageid'),
                             caption=f'<b>Причина отмены:</b>\n<i>{message.text}</i>',
                             reply_markup=cancelordelete, parse_mode= ParseMode.HTML)   

async def backcall(call:CallbackQuery, bot:Bot, state: FSMContext):
    if call.data == 'cash':
        file='AgACAgIAAxkDAAIH0GW0RdAGS-_opEpGi4j9XzVLZ710AALx2TEbZ7ahSYlTIm7KV97iAQADAgADbQADNAQ'
        text = '*Совет:*\n_Указывайте Ваш `@username` при оплате\.\nЭто ускорит обработку пополнения\._'
        msg = await call.message.edit_media(InputMediaPhoto(media = file,
                                        caption=text, parse_mode=ParseMode.MARKDOWN_V2), reply_markup=pay_inline)
    
    if call.data == 'delete':
        if await delete_file(call.message.document.file_unique_id) == 0:
            await call.answer('Файл уже удалён из базы данных')
        await call.answer('Файл удалён из базы данных')
        await call.message.delete()
        
    if call.data.startswith('statusfile:'):
        status = call.data.split(':')[1]
        list_files = InlineKeyboardBuilder()
        files = await get_all_files_in_status(status)
        if status == 'done': text1 = 'Напечатанные файлы'
        if status == 'queue': text1 = 'Файлы в очереди'
        if status == 'canceled': text1 = 'Отмененные файлы'
        if files == []:
            await call.message.edit_text(f'<i>{text1} отсутствуют.</i>', parse_mode=ParseMode.HTML, reply_markup=statuschange)
        else:
            for file in files:
                unique_id, user_id, date, file_name = file
                if len(f"{date} - {file_name} - @{await get_username(user_id)}") > 50:
                    file_name = file_name[:15]+'...'
                list_files.button(text=f"{date} | {file_name} | @{await get_username(user_id)}", callback_data=f"userfile:{unique_id}")
            list_files.adjust(1)
            list_files.row(
                            InlineKeyboardButton
                        (
                            text='Готовые',
                            callback_data=f"statusfile:done"
                            ),
                            InlineKeyboardButton
                            (
                            text='Ожидают',
                            callback_data=f"statusfile:queue"
                            ),
                            InlineKeyboardButton
                            (
                            text='Отменены',
                            callback_data=f"statusfile:canceled"
                            )
            )
            await call.message.edit_text(f'<i>{text1}:</i>', reply_markup=list_files.as_markup(), parse_mode=ParseMode.HTML)
    
    if call.data.startswith('myfile:'):
        unique_id = call.data.split(':')[1]
        try:
            fileinfo = await get_fileinfo(unique_id)
            if fileinfo[4] == 'queue':
                await bot.send_document(fileinfo[1],fileinfo[0],
                                caption='<i>Файл ожидает печати.</i>',
                                parse_mode=ParseMode.HTML, reply_markup=cancel)
            elif fileinfo[4] == 'done':
                await bot.send_document(fileinfo[1],fileinfo[0],
                                caption='<i>Файл напечатан!</i>',
                                parse_mode=ParseMode.HTML,
                                reply_markup=delete)                
            elif fileinfo[4] == 'canceled':
                await bot.send_document(fileinfo[1],fileinfo[0],
                                caption='<i>Файл снят с очереди на печать!</i>',
                                parse_mode=ParseMode.HTML,
                                reply_markup=delete)                
        except:
            await call.answer('Файла не существует...')
    
    if call.data.startswith('userfile:'):
        unique_id = call.data.split(':')[1]
        try:
            fileinfo = await get_fileinfo(unique_id)
            if fileinfo[4] == 'queue':
                await bot.send_document(os.getenv('ADMIN_ID'), fileinfo[0], 
                                caption=f'<i>От пользователя @{await get_username(fileinfo[1])}\
                                \n Дата: <code>{fileinfo[2]}</code></i>',
                                parse_mode=ParseMode.HTML, reply_markup=cancelorprint)
            elif fileinfo[4] == 'done':
                await bot.send_document(os.getenv('ADMIN_ID'),fileinfo[0],
                                caption='<i>Файл напечатан!</i>',
                                parse_mode=ParseMode.HTML)                
            elif fileinfo[4] == 'canceled':
                await bot.send_document(os.getenv('ADMIN_ID'),fileinfo[0],
                                caption='<i>Файл снят с очереди на печать!</i>',
                                parse_mode=ParseMode.HTML)                
        except:
            await call.answer('Файла не существует...')

    if call.data == 'file:adminprint':
        fileinfo = await get_fileinfo(call.message.document.file_unique_id)
        await edit_file_status(call.message.document.file_unique_id,'done')
        await bot.send_document(fileinfo[1],call.message.document.file_id,
                                caption='<i>Файл напечатан!</i>',
                                parse_mode=ParseMode.HTML)
        await call.message.edit_caption(
                                caption=f'<i>Файл напечатан!</i>', 
                                reply_markup = None,
                                parse_mode=ParseMode.HTML)

    if call.data.startswith('delete:'):
        if call.data == 'delete:accept':
            comment = await state.get_data()
            comment = comment.get("comment")
            if comment is None:
                comment = '<code>Не указано</code>'
            fileinfo = await get_fileinfo(call.message.document.file_unique_id)
            await edit_file_status(call.message.document.file_unique_id,'canceled')
            await edit_user_balance(fileinfo[1],round(await get_balance(fileinfo[1])+fileinfo[3],2))
            await bot.send_document(fileinfo[1],call.message.document.file_id,
                                    caption=f'Файл снят с очереди на печать!\
                                    \nЗатраченные средства возвращены.\n\
                                    \n<b>Причина отмены:</b>\n<i>{comment}</i>',
                                    parse_mode=ParseMode.HTML)
            await call.message.edit_caption(caption=f'<i>Файл снят с очереди на печать!</i>', 
                                reply_markup = None,
                                parse_mode=ParseMode.HTML)
            await state.clear()
        else:
            await state.clear()
            fileinfo = await get_fileinfo(call.message.document.file_unique_id)
            await call.message.edit_caption( 
                                    caption=f'<i>От пользователя @{await get_username(fileinfo[1])}\
                                    \n Дата: <code>{fileinfo[2]}</code></i>',
                                    parse_mode=ParseMode.HTML, reply_markup=cancelorprint)

    if call.data == 'file:admincancel':
        try:
            unique_id = call.message.document.file_unique_id
            fileinfo = await get_fileinfo(unique_id)
            if fileinfo[4] == 'queue':
                await call.message.edit_caption(
                    caption='<i>Укажите причину отмены.</i>', 
                    reply_markup=canceldelete, 
                    parse_mode=ParseMode.HTML)
                await state.set_state(Comment.COMMENT)
                await state.update_data(messageid = call.message.message_id)
            elif fileinfo[4] == 'done':
                await call.answer('Файл уже напечатан!')
                await call.message.delete()
            elif fileinfo[4] == 'canceled':
                await call.answer('Файл уже снят с очереди на печать!')
                await call.message.delete_reply_markup()
        except:
            await call.answer('Файла не существует...')
        
    if call.data == 'file:usercancel':
        try:
            fileinfo = await get_fileinfo(call.message.document.file_unique_id)
            if fileinfo[4] == 'queue':
                await edit_file_status(call.message.document.file_unique_id,'canceled')
                await edit_user_balance(fileinfo[1],round(await get_balance(fileinfo[1])+fileinfo[3],2))
                await call.message.edit_caption(caption=f'<i>Файл снят с очереди на печать!</i>',
                                parse_mode=ParseMode.HTML, reply_markup=delete)
                await call.answer('Файл снят с очереди на печать!')
            elif fileinfo[4] == 'done':
                await call.answer('Файл уже напечатан!')
                await call.message.edit_caption(caption=f'<i>Файл уже напечатан!</i>',
                                parse_mode=ParseMode.HTML, reply_markup=delete)
            elif fileinfo[4] == 'canceled':
                await call.answer('Файл уже снят с очереди на печать!')
                await call.message.edit_caption(caption=f'<i>Файл уже снят с очереди на печать!</i>',
                                parse_mode=ParseMode.HTML, reply_markup=delete)
        except:
            await call.answer('Файла не существует...')
            
    if call.data.startswith('newfile:'):
        if call.data.startswith('newfile:accept:'):
            price = float(call.data.split(':')[2])
            balance = await get_balance(call.from_user.id)
            if balance is None:
                await create_user(call.from_user.id, call.from_user.username)
                balance = 0.0
            if round(balance-price, 2) > 0:
                await create_file(call.message.document.file_unique_id, 
                                  call.message.document.file_id, 
                                  call.from_user.id, price, 
                                  call.message.document.file_name)
                await edit_user_balance(call.from_user.id, round(balance-price, 2))
                await call.answer('Файл принят в очередь на печать!')
                await call.message.edit_caption(caption=f'<i>Файл принят в очередь на печать!</i>',
                                parse_mode=ParseMode.HTML, reply_markup=cancel)
                await asyncio.sleep(900)
                fileinfo = await get_fileinfo(call.message.document.file_unique_id)
                if fileinfo[4] == 'queue':
                    await bot.send_document(os.getenv('ADMIN_ID'), fileinfo[0], 
                                caption=f'<i>От пользователя @{await get_username(fileinfo[1])}\
                                \n Дата: <code>{fileinfo[2]}</code></i>',
                                parse_mode=ParseMode.HTML, reply_markup=cancelorprint)

            else:
                await call.answer('Недостаточно средств!', show_alert=True)
        else:
            await call.message.delete()
            await call.answer('Сомнительно, но окэй 👌')