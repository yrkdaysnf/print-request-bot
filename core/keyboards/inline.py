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

cancel = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='✗ Отменить',
            callback_data=f"file:usercancel"
        )
    ]
]
)


cancelorprint = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='✗ Отменить',
            callback_data=f"file:admincancel"
        ),
        InlineKeyboardButton(
            text='🖨 Распечатать',
            callback_data=f"file:adminprint"
        ),
    ]
]
)

canceldelete = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Я передумал',
            callback_data=f"delete:cancel"
        )
    ]
]
)

cancelordelete = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Я передумал',
            callback_data=f"delete:cancel"
        ),
        InlineKeyboardButton(
            text='Продолжить',
            callback_data=f"delete:accept"
        ),
    ]
]
)