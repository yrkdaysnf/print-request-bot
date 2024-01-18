from aiogram import Bot
from aiogram.types import Message
from core.keyboards.start import main_keyboard
from core.data.sql import create_user


async def get_start(message: Message, bot = Bot):
    await create_user(user_id=message.from_user.id, username=message.from_user.username)
    await message.answer(f'''Привет {message.from_user.full_name}!
Добро пожаловать в систему автоматизированной печати!
Для продолжения, нажми на самую красивую кнопочку.''', reply_markup=main_keyboard)
    
async def echo(message:Message):
    await message.answer('idk bro')