from aiogram import Bot
from aiogram.types import Message
from core.keyboards.start import main_keyboard

async def get_start(message: Message, bot = Bot):
    await message.answer(f'Привет {message.from_user.first_name}!\nДобро пожаловать в систему автоматизированной печати внутри бота Telegram. Для продолжения, нажми на самую красивую кнопку.',
                         reply_markup=main_keyboard)

async def echo(message:Message):
    await message.answer('idk bro')