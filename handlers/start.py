# handlers/start.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import register_user

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    telegram_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name

    register_user(
        telegram_id,
        username
    )

    await message.answer(
        """
Добро пожаловать в магазин электроники 📱

Доступные команды:

/catalog - Каталог товаров
/cart - Корзина
"""
    )