import os
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, Message
from core.keyboards.start import main_keyboard, admin_keyboard


async def commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы.'
        ),
        BotCommand(
            command='help',
            description='Как пользоваться?'
        ),
        BotCommand(
            command='about',
            description='О боте и его авторе.'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

def adminoruser(id):
    if id == int(os.getenv('ADMIN_ID')):
        return admin_keyboard
    else:
        return main_keyboard