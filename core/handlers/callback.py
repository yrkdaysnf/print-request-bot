import os
from aiogram import Bot
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from core.keyboards.inline import pay_inline, cash_inline
from aiogram.enums import ParseMode

async def backcall(call:CallbackQuery, bot:Bot):
    # for user in await get_all_users():
    #     user_id, username, balance = user
    #     if call.data == f'id:balance:{user_id}':
    #         text = f'Пользователь @{username}\nБаланс {balance}₽ Что будем делать?'
    #         await call.message.edit_text(text, reply_markup=cash_inline)

    if call.data == 'cash':
        if call.message.from_user.id != int(os.getenv('ADMIN_ID')):
            text = '*Совет:*\n_Указывайте Ваш `@username` при оплате\.\nЭто ускорит обработку пополнения\._'
            await call.message.edit_media(InputMediaPhoto(media = FSInputFile('core\\data\\files\\resources\\qr-code.jpg'),
                                                        caption=text, parse_mode=ParseMode.MARKDOWN_V2), reply_markup=pay_inline)
