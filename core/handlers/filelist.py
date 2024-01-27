from aiogram import Bot
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.enums import ParseMode
from core.keyboards.inline import statuschange
from core.data.sql import get_all_myfiles, get_all_files_in_status, get_username


async def myfilelist(message:Message):
    statuslist = {'canceled':'Отменён','queue':'Ожидает','done':'Готов'}
    list_files = InlineKeyboardBuilder()
    files = await get_all_myfiles(message.from_user.id)
    if files == []:
        await message.answer('<i>Список файлов пуст.</i>', parse_mode=ParseMode.HTML)
    else:
        for file in files:
            unique_id, date, status, file_name = file
            status = statuslist.get(status)
            if len(f"{date} - {file_name} - {status}") > 50:
                file_name = file_name[:15]+'...'
            list_files.button(text=f"{date} | {file_name} | {status}", callback_data=f"myfile:{unique_id}")
        list_files.adjust(1)
        await message.answer('<i>Список файлов:</i>', reply_markup=list_files.as_markup(), parse_mode=ParseMode.HTML)

async def fileinqueue(message:Message):
    list_files = InlineKeyboardBuilder()
    files = await get_all_files_in_status('queue')
    if files == []:
        await message.answer('<i>Файлы в очереди отсутсвуют.</i>', parse_mode=ParseMode.HTML, reply_markup=statuschange)
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
        await message.answer('<i>Файлы в очереди:</i>', reply_markup=list_files.as_markup(), parse_mode=ParseMode.HTML)