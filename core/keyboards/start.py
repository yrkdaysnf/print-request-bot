from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text= '💳 Баланс'
        ),
        KeyboardButton(
            text='📂 Мои файлы'
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Что будем делать?')

admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text= '💳 Баланс пользователей'
        )
    ],   
    [
        KeyboardButton(
            text='🧭 Файлы в очереди'
        ),
        KeyboardButton(
            text='🖨 Принтер'
        ) 
    ]
],resize_keyboard=True, input_field_placeholder='Что будем делать?', one_time_keyboard=True)