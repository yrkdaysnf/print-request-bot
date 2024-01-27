from aiogram import Bot
from aiogram.types import Message, FSInputFile
from core.keyboards.inline import cash_inline
from core.data.sql import get_balance, create_user
from aiogram.enums import ParseMode

async def wannapay(message:Message, bot:Bot):
    file = "AgACAgIAAxkDAAIH0GW0Rc4koq-2fwcjeUr01dkGI2jIAALw2TEbZ7ahST98Lpxs6StRAQADAgADcwADNAQ"
    balance = await get_balance(message.from_user.id)
    if balance is None:
        await create_user(message.from_user.id, message.from_user.username)
        balance = 0
    msg = await bot.send_photo(message.chat.id,file,
                         caption=f'<i>Ваш текущий баланс: <code>{balance}</code></i> ₽',
                         reply_markup=cash_inline, parse_mode=ParseMode.HTML)
