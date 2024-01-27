import logging, asyncio, os, datetime
from dotenv import load_dotenv as ld
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from core.util.statesform import Comment
from core.handlers.basic import get_start, echo, start_bot, stop_bot, printer
from core.handlers.balance import listofusers, edit_balance
from core.handlers.filelist import myfilelist, fileinqueue
from core.handlers.status import edit_status, statusinfo
from core.handlers.callback import backcall, get_comment
from core.data.files.resources.info import help, about
from core.handlers.files import sendfile
from core.handlers.pay import wannapay


ld()
TOKEN = os.getenv('API_TOKEN')


logging.basicConfig(level=logging.INFO, 
                    filename=f'core\\data\\files\\logs\\printbot_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log',
                    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s')
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.callback_query.register(backcall)
    dp.message.register(sendfile, F.document)
    dp.message.register(get_comment, Comment.COMMENT)
    dp.message.register(get_start, Command('start'))
    dp.message.register(help, Command('help'))
    dp.message.register(about, Command('about'))
    dp.message.register(edit_balance, Command('b'), F.from_user.id==int(os.getenv('ADMIN_ID')))
    dp.message.register(edit_status, Command('s'), F.from_user.id==int(os.getenv('ADMIN_ID')))
    dp.message.register(listofusers, F.text.startswith('💳'), F.from_user.id==int(os.getenv('ADMIN_ID')))
    dp.message.register(fileinqueue, F.text.startswith('🧭'), F.from_user.id==int(os.getenv('ADMIN_ID')))
    dp.message.register(statusinfo, F.text == '🖨 Принтер', F.from_user.id==int(os.getenv('ADMIN_ID')))
    dp.message.register(wannapay, F.text.startswith('💳') | (F.text == '/balance'))
    dp.message.register(myfilelist, F.text.startswith('📂') | (F.text == '/myfiles'))
    dp.message.register(printer, F.text == '🖨')
    dp.message.register(echo)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())