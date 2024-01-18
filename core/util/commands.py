from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


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