import logging, asyncio
from dotenv import dotenv_values
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from core.data.sql import db_start
from core.handlers.basic import get_start, echo
#from core.util.commands import commands
#from core.middlewares.printernotwork import CounterMiddleware


TOKEN = dotenv_values('.env')['API_TOKEN']
ADMIN = dotenv_values('.env')['ADMIN_ID']

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s')
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def start_bot(bot: Bot):
    #await commands(bot)
    await db_start()
    await bot.send_message(ADMIN,text='Запуск',disable_notification=True)

async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN,text='Остановка',disable_notification=True)

async def main():
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_start, Command('start'))
    dp.message.register(echo)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())