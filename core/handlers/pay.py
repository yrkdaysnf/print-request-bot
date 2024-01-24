from aiogram import Bot
from aiogram.types import Message, FSInputFile
from core.keyboards.inline import cash_inline
from core.data.sql import get_balance
from aiogram.enums import ParseMode

async def wannapay(message:Message, bot:Bot):
    balance = await get_balance(message.from_user.id)
    await bot.send_photo(message.chat.id,FSInputFile('core\\data\\files\\resources\\ahtung.png'),
                         caption=f'<i>Ваш текущий баланс: <code>{balance}</code></i> ₽',
                         reply_markup=cash_inline, parse_mode=ParseMode.HTML)