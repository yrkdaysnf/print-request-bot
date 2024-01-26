from aiogram import Bot
from aiogram.types import Message
from aiogram.filters import CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.data.sql import get_all_users, edit_user_balance, get_balance, get_username
from aiogram.enums import ParseMode


async def edit_status():
    return None

async def statusinfo(message:Message):
    return None