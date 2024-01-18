from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

back_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Назад'
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Что будем делать?', selective=True)