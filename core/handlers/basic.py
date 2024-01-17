from aiogram import Bot
from aiogram.types import Message
from core.keyboards.reply import main_keyboard

async def get_start(message: Message, bot = Bot):
    await message.answer(f'Привет {message.from_user.first_name}.\nТвой id: {message.from_user.id}\n{message.from_user.full_name}', reply_markup=main_keyboard)

async def echo(message:Message):
    await message.answer('idk bro')