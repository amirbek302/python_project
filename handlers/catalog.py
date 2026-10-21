# handlers/catalog.py

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from storage import user_orders
from database import get_products, get_product_by_id
from models import Order, Phone, Laptop
from states import ShopState

router = Router()

@router.message(Command("catalog"))
async def catalog_handler(message: types.Message, state: FSMContext):
    await state.set_state(ShopState.catalog)
    products = get_products()

    if not products:
        await message.answer("📦 Каталог пока пуст.")
        return

    buttons = []

    for product_id, name, price, photo in products:
        if "iphone" in name.lower() or "samsung" in name.lower():
            product = Phone(product_id, name, price, photo)
        else:
            product = Laptop(product_id, name, price, photo)

        buttons.append(
            [KeyboardButton(text=product.name)]
        )

    buttons.append([KeyboardButton(text="❌ Закрыть")])

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )

    await message.answer("📱 Выберите товар:", reply_markup=keyboard)

# /////////
@router.callback_query(F.data.startswith("add_"))
async def add_to_cart(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split("_")[1])

    user_id = callback.from_user.id

    if user_id not in user_orders:
        user_orders[user_id] = Order()

    name, price, photo = get_product_by_id(product_id)

    if "iphone" in name.lower() or "samsung" in name.lower():
        product = Phone(product_id, name, price, photo)
    else:
        product = Laptop(product_id, name, price, photo)

    user_orders[user_id].add_product(product)

    await callback.answer("✅ Товар добавлен")
    await callback.message.answer(
        f"Сейчас в корзине товаров: {len(user_orders[user_id].get_products())}"
    )

# /////
@router.message(ShopState.catalog,F.text)
async def product_handler(message: types.Message, state: FSMContext):
    if message.text.startswith("/"):
        return

    if message.text == "❌ Закрыть":
        await state.clear()

        await message.answer(
            "Каталог закрыт.",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    products = get_products()

    for product_id, name, price, photo in products:
        if message.text == name:
            if "iphone" in name.lower() or "samsung" in name.lower():
                product = Phone(product_id, name, price, photo)
            else:
                product = Laptop(product_id, name, price, photo)

            image = FSInputFile(product.photo)

            builder = InlineKeyboardBuilder()
            builder.button(
                text="🛒 Добавить в корзину",
                callback_data=f"add_{product.product_id}"
            )

            await message.answer_photo(
                photo=image,
                caption=product.get_info(),   # OOP
                reply_markup=builder.as_markup()
            )

            return

    await message.answer("Товар не найден.")
