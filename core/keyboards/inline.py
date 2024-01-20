from dotenv import dotenv_values as dv
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


cash_inline = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Пополнить',
            callback_data='cash'
        )
    ]
]
)

pay_inline = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Оплатить',
            url=dv('.env')['PAY_URL']
        )
    ]
]
)