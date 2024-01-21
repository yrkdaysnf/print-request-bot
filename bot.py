import logging, asyncio, os
from dotenv import load_dotenv as ld
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject
from core.handlers.basic import get_start, echo, start_bot, stop_bot
from core.handlers.pay import wannapay
from core.handlers.balance import listofusers
from core.handlers.callback import backcall


ld()
TOKEN = os.getenv('API_TOKEN')


logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s')
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_start, Command('start'))
    dp.message.register(wannapay, F.text == '💳 Баланс')
    dp.message.register(listofusers, F.text == '💳 Баланс пользователей', )
    dp.callback_query.register(backcall)
    dp.message.register(echo)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())