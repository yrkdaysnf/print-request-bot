from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text= '💳 Пополнить баланс'
        ),
        KeyboardButton(
            text='🧭 Проверка статуса печати'
        )
    ],
    [
        KeyboardButton(
            text='🎁 Отправить файлы на печать'
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Что будем делать?', selective=True)

admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text= '💳 Баланс пользователей'
        ),
        KeyboardButton(
            text='🧭 Файлы в очереди'
        )
    ],
    [
        KeyboardButton(
            text='Статус принтера'
        )
    ]
])