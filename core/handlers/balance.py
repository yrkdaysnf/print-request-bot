from aiogram import Bot
from aiogram.types import Message
from aiogram.filters import CommandObject
from core.data.sql import get_all_users, edit_user_balance, get_balance, get_username
from aiogram.enums import ParseMode


async def listofusers(message:Message):
    users = await get_all_users()
    response_text = '<i>Список пользователей и их баланс:</i>\n\n'
    for user in users:
        user_id, username, balance = user
        response_text += f"<code>{user_id}</code> - @{username} - {balance}₽\n"
    response_text += '\n <i>Для изменения баланса, воспользуйтесь командой:\
                      \n<code>/b (id) (число)</code>\
                      \nДля десятичных дробей используйте точку.</i>'
    await message.answer(f'{response_text}', parse_mode=ParseMode.HTML, reply_markup=None)

async def edit_balance(message:Message, command:CommandObject, bot:Bot):
    try:
        data = command.args.split()    
        if len(data) != 2:
            raise ValueError("Некорректное количество аргументов")
        user_id = data[0]
        username = await get_username(user_id)
        new_balance = round(await get_balance(user_id) + float(data[1]),2)
        await edit_user_balance(user_id, new_balance)
        await message.reply(f'Баланс для @{username} изменён на {data[1]}₽!\
                            \nТекущий баланс: {new_balance}₽')
        await bot.send_message(user_id,text=f'<i>Ваш баланс был изменён на {data[1]}</i>₽<i>!\
                               \nТекущий баланс: {new_balance}</i>₽', parse_mode=ParseMode.HTML)
    except TypeError as e:
        await message.reply(f'Ошибка типа данных: {e}')
    except ValueError as e:
        await message.reply(f'Ошибка: {e}')
    except Exception as e:
        await message.reply(f'Произошла ошибка: {e}')