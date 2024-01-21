from aiogram import Bot
from aiogram.types import Message
from core.data.sql import create_user, db_start
from core.util.commands import adminoruser, commands


async def start_bot(bot: Bot):
    await commands(bot)
    await db_start()
    print('Start')

async def stop_bot(bot: Bot):
    print('Stop')

async def get_start(message: Message, bot = Bot):
        await create_user(user_id=message.from_user.id, username=message.from_user.username)
        await message.answer(f'''Здравствуйте, {message.from_user.first_name}.
Добро пожаловать в систему автоматизированной печати!
Для продолжения, нажмите на одну из интересующих Вас кнопок.''', reply_markup=adminoruser(message.from_user.id))

async def echo(message:Message):
    await message.reply('idk bro', reply_markup=adminoruser(message.from_user.id))