from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import dotenv_values as dv


PAY_URL = dv('.env')['PAY_URL']

pay_inline = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='По ссылке',
            url=PAY_URL
        )
    ],
    [
        InlineKeyboardButton(
            text='По QR коду',
            callback_data='qrcode'
        )
    ]
]
)