from aiogram import Bot
from aiogram.types import Message
from aiogram.enums import ParseMode
from core.data.sql import create_user, db_start
from core.util.commands import commands
from core.util.check import is_admin
from core.keyboards.start import main_keyboard, admin_keyboard


async def start_bot(bot: Bot):
    await commands(bot)
    await db_start()
    print('START')

async def stop_bot():
    print('STOP')

async def printer(message: Message):
    await message.answer('🖨')

async def get_start(message: Message, bot = Bot):
    file = 'AgACAgIAAxkDAAIHIGW0A_glqlaEbe3Pa8Tc-8Rez5YIAALv2TEbZ7ahSdb74hhD60KMAQADAgADcwADNAQ'
    text=f'''
Здравствуйте, <i>{message.from_user.full_name}</i>!
Добро пожаловать в систему автоматизированной печати!
Отправьте мне файлы или воспользуйтесь командами.

<i><b>Список команд:</b></i>
💳 <i>/balance</i> — Ваш баланс.
📂 <i>/myfiles</i> — Ваши файлы.

🤝 <i>/help</i> — Как пользоваться?
📣 <i>/about</i> — О боте и его авторе.

<tg-spoiler>🔥 <i>/delete</i> — Разорвать все связи.</tg-spoiler>
'''
    if is_admin(message.from_user.id) == True: keyboard = admin_keyboard
    else: keyboard = main_keyboard
    await create_user(user_id=message.from_user.id, username=message.from_user.username)
    await bot.send_photo(chat_id=message.chat.id,photo=file,caption=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)


async def echo(message:Message):
    if is_admin(message.from_user.id) == True: keyboard = admin_keyboard
    else: keyboard = main_keyboard
    await message.reply('Я не знаю такой команды 🥺', reply_markup=keyboard)