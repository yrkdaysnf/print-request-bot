from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.data.sql import get_all_users


async def listofusers(message:Message, bot:Bot):  
    list_users = InlineKeyboardBuilder()
    users = await get_all_users()
    for user in users:
        user_id, username, balance = user
        list_users.button(text=f"@{username} - {balance}₽", callback_data=f"{user_id}")
    list_users.adjust(1)

    await message.answer('Список пользователей:', reply_markup=list_users.as_markup())