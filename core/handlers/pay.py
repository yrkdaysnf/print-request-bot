from aiogram import Bot
from aiogram.types import Message
from core.keyboards.back import back_keyboard
from core.keyboards.inline import pay_inline
from core.data.sql import get_balance


async def pay(message:Message, bot:Bot):
    balance = await get_balance(message.from_user.id)
    await message.answer(f'''Ваш текущий баланс: {balance} ₽ \n\n\
Для пополнения баланса, выберите один из вариантов ниже. Укажите сумму и ожидайте пополнения. 
На это может потребоваться некоторое время, потому как эта операция обрабатывается вручную.''',
reply_markup=pay_inline)