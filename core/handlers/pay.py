from aiogram import Bot
from aiogram.types import Message, FSInputFile
from core.keyboards.inline import cash_inline
from core.data.sql import get_balance


async def wannapay(message:Message, bot:Bot):
    balance = await get_balance(message.from_user.id)
    await bot.send_photo(message.chat.id,FSInputFile('core\\data\\files\\resources\\ahtung.png'),
                         caption=f'Ваш текущий баланс: {balance} ₽', 
                         reply_markup=cash_inline)