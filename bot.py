import logging, asyncio, os, datetime
from dotenv import load_dotenv as ld
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from core.handlers.basic import get_start, echo, start_bot, stop_bot
from core.handlers.pay import wannapay
from core.handlers.balance import listofusers, edit_balance
from core.handlers.callback import backcall, get_comment
from core.handlers.files import sendfileinfo, sendfile
from core.util.statesform import Comment


ld()
TOKEN = os.getenv('API_TOKEN')


logging.basicConfig(level=logging.INFO, 
                    filename=f'core\\data\\files\\logs\\printbot_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log',
                    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s')
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_comment, Comment.COMMENT)
    dp.message.register(get_start, Command('start'))
    dp.message.register(edit_balance, Command('b', 'balance'))
    dp.message.register(sendfile, F.document)
    dp.message.register(wannapay, F.text == '💳 Баланс')
    dp.message.register(listofusers, F.text == '💳 Баланс пользователей')
    dp.message.register(sendfileinfo, Command('help'))
    dp.callback_query.register(backcall)
    dp.message.register(echo)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())