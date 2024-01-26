import os, asyncio, logging
from aiogram import Bot
from aiogram.types import Message, FSInputFile, InputMediaDocument
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.data.sql import get_fileinfo
from core.util.file import price_alg
from docx2pdf import convert as d2p


ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx'}

async def sendfileinfo(message:Message, bot:Bot):
    await bot.send_photo(message.chat.id,FSInputFile('core\\data\\files\\resources\\start.jpg'),caption=
f'Для создания заявки на печать, просто отправьте файл.\n\
\n<i>Принимаемые расширения:</i>\n<code>.pdf .doc .docx</code>\n\
\nПосле отправки потребуется некоторое время для расчета итоговой стоимости,\
далее вам предложит подтвердить создание новой задачи печати.', 
parse_mode=ParseMode.HTML)

async def sendfile(message:Message, bot:Bot):
    if message.document.file_size <= 10485760:
        name, ext = os.path.splitext(message.document.file_name)
        if ext in ALLOWED_EXTENSIONS:
            if await get_fileinfo(message.document.file_unique_id) != None:
                await message.reply(f'<i>Файл <code>{name}</code> уже находится в очереди на печать!</i>',
                                    parse_mode=ParseMode.HTML)
            else:
                path = f'core\\data\\files\\temp\\{message.from_user.id}'
                if not os.path.exists(path):os.makedirs(path)
                pdf = f'{path}\\{name}.pdf'
                tempath = f'{path}\\{message.document.file_name}'
                file_id = message.document.file_id
                file_info = await bot.get_file(file_id)
                file_path = file_info.file_path
                downloaded_file = await bot.download_file(file_path)
                with open(tempath, "wb") as new_file:
                    new_file.write(downloaded_file.read())
                    
                msg = await bot.send_document(message.chat.id, file_id, 
                                    caption=f'<i>Файл <code>{name}</code> принят!</i>',
                                    parse_mode=ParseMode.HTML)
                await asyncio.sleep(2)
                if ext != '.pdf':
                    await bot.edit_message_caption(message.chat.id, msg.message_id,
                                        caption=f'<i>Файл: <code>{name}</code> принят!\
                                        \n\n<b>Произвожу конвертацию {ext} --> .pdf</b></i>',
                                        parse_mode=ParseMode.HTML)

                    d2p(tempath)
                    os.remove(tempath)
                        
                    msg = await bot.edit_message_media(InputMediaDocument(media=FSInputFile(pdf),
                                        caption=f'<i>Файл: <code>{name}</code> принят!\
                                        \n\n<b>Произвожу оценку стоимости...</b></i>',
                                        parse_mode=ParseMode.HTML),
                                        message.chat.id, msg.message_id)
                                        
                await bot.edit_message_caption(message.chat.id, msg.message_id,
                                    caption=f'<i>Файл: <code>{name}</code> принят!\
                                    \n\n<b>Произвожу оценку стоимости...</b></i>',
                                    parse_mode=ParseMode.HTML)
                
                pages, fill = await price_alg(pdf)
                if pages == 0:
                    await bot.delete_message(message.chat.id, msg.message_id)
                    await bot.send_message(message.chat.id,'🤡', protect_content=True)
                else:
                    price = f'{(pages+fill*50):.2f}'

                    newfile = InlineKeyboardBuilder()
                    newfile.button(text='✗ Отменить', callback_data=f'newfile:cancel')
                    newfile.button(text='✓ Продолжить', callback_data=f'newfile:accept:{price}')
                    newfile.adjust(2)


                    await bot.edit_message_caption(message.chat.id, msg.message_id,
                                        caption=f'<i>Файл: <code>{name}</code>{ext}\n\
                                        \nКоличество листов: <code>{pages}</code>\
                                        \nСредняя заполненность: <code>{int(fill*100/pages)}%</code>\
                                        \nCтоимость печати: <code>{price}</code></i> ₽',
                                        parse_mode=ParseMode.HTML, reply_markup=newfile.as_markup())
                os.remove(pdf)
        else:
            await message.reply(
                f'<i><b>Ой, файл не того формата!</b>\
                \n\nЯ принимаю только:</i>\
                \n<b>Файлы менее</b> <code>10</code> мб\
                \n<code>.pdf .doc .docx</code>', parse_mode=ParseMode.HTML)
    else:
        await message.reply(
                f'<i><b>Ой, файл слишком большой!</b>\
                \n\nЯ принимаю только:</i>\
                \n<b>Файлы менее</b> <code>10</code> мб\
                \n<code>.pdf .doc .docx</code>', parse_mode=ParseMode.HTML)