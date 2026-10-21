# main.py
import asyncio

from aiogram import Bot, Dispatcher

# config все подключение с тг
from config import TOKEN

# handlers/start.py <- all for start command
from handlers.start import router as start_router

# handlers/catalog.py <- all for catalog command
from handlers.catalog import router as catalog_router

# handlers/cart.py <- all for cart command
from handlers.cart import router as cart_router

# подключение
bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(catalog_router)
dp.include_router(cart_router)

print(dp)

# /#/////#//////#/////#////#///////#//////#/////#///////////#////////#////////#//////#//////#////
async def main():
    await dp.start_polling(bot)

asyncio.run(main())


# в постгрессе 250