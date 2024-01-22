from aiogram import Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from core.data.sql import get_all_users
from core.keyboards.inline import pay_inline


async def backcall(call:CallbackQuery, bot:Bot, message:Message):

    for user in await get_all_users():
        user_id, username, balance = user
        if call.data == f'id:balance:{user_id}':
            text = f'Выбран пользователь @{username}, его баланс {balance}₽\n Что будем делать?'
            await bot.message.answer(text, reply_markup=None)

    if call.data == 'cash':
        await call.message.edit_media(InputMediaPhoto(media = FSInputFile('core\\data\\files\\resources\\qr-code.jpg')),
                                    reply_markup=pay_inline)
