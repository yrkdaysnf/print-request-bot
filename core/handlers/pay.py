from aiogram import Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from core.keyboards.inline import pay_inline, cash_inline
from core.data.sql import get_balance


async def wannapay(message:Message, bot:Bot):
    balance = await get_balance(message.from_user.id)
    await bot.send_photo(message.chat.id,FSInputFile('core\\data\\file\\resourses\\ahtung.png'),
                         caption=f'Ваш текущий баланс: {balance} ₽', 
                         reply_markup=cash_inline)

async def pay(call:CallbackQuery, bot:Bot):
    if call.data == 'cash':
        await call.message.edit_media(InputMediaPhoto(media = FSInputFile('core\\data\\file\\resourses\\qr-code.jpg')),
                                    reply_markup=pay_inline)