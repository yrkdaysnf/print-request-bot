import os, asyncio, shutil
from aiogram import Bot
from aiogram.types import Message, InputFile
from aiogram.enums import ParseMode
from aiogram.filters import CommandObject

async def sendfileinfo(message:Message):
    await message.answer(f'Для создания заявки на печать, просто отправьте один или несколько файлов.\n\
                         \n<i>Бот принимает:</i> <code>.pdf .doc .docx</code>\
                         \nПосле отправки потребуется некоторое время для расчета итоговой стоймости, далее вам предстоит выбрать дополнительные параметры и подтвердить создание новой задачи печати.\n\
                         \n<b>ВАЖНО:</b>\n<i>При отправке нескольких файлов, они будут объединены в один.</i>', parse_mode=ParseMode.HTML)
    
async def sendfile(message:Message, bot:Bot):
    # Проверяем, есть ли файлы в сообщении
    if message.document:
        # Получаем информацию о файле
        file_info = await bot.get_file(message.document.file_id)
        file_path = file_info.file_path
        path = f'core\\data\\files\\temp\\{message.from_user.id}'
        if not os.path.exists(path):os.makedirs(path)
 
        # Скачиваем файл и сохраняем его
        downloaded_file = await bot.download_file(file_path)
        with open(f'{path}\\{message.document.file_name}', "wb") as new_file:
            new_file.write(downloaded_file.read())

        await asyncio.sleep(10)

        shutil.rmtree(path)