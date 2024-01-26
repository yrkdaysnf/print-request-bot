from aiogram import Bot
from aiogram.types import Message
from core.data.sql import create_user, db_start
from core.util.commands import commands
from core.util.check import is_admin
from core.keyboards.start import main_keyboard, admin_keyboard


async def start_bot(bot: Bot):
    await commands(bot)
    await db_start()
    print('Start')

async def stop_bot(bot: Bot):
    print('Stop')

async def get_start(message: Message, bot = Bot):
    if is_admin(message.from_user.id) == True: keyboard = admin_keyboard
    else: keyboard = main_keyboard
    await create_user(user_id=message.from_user.id, username=message.from_user.username)
    await message.answer(
f'''Здравствуйте, {message.from_user.first_name}!
Добро пожаловать в систему автоматизированной печати!
Для продолжения, воспользуйтесь кнопками ниже или оптравьте файл.''', reply_markup=keyboard)

async def echo(message:Message):
    if is_admin(message.from_user.id) == True: keyboard = admin_keyboard
    else: keyboard = main_keyboard
    await message.reply('Я не знаю такой команды 🥺', reply_markup=keyboard)