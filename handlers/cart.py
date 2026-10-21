# handlers/cart.py
import asyncio
from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import (
    get_client_id,
    get_product_by_id,
    create_order,
    add_product_to_order,
    complete_order
)
from storage import user_orders
from models import Phone, Laptop, Order

router = Router()

@router.message(Command("cart"))
async def cart_handler(message: types.Message, state: FSMContext):
    # print(await state.get_state())
    # print(await state.get_data())
    # print("CART WORKS")

    user_id = message.from_user.id

    if user_id not in user_orders:
        await message.answer("🛒 Корзина пока пустая.")
        return

    order = user_orders[user_id]

    text = "🛒 Ваша корзина:\n\n"
    total = 0

    for product in order.get_products():
        text += product.get_info() + "\n"

    text += f"\n💰 Итого: {order.total_price()}$"

    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Оформить заказ", callback_data="checkout")
    builder.button(text="🗑 Очистить корзину", callback_data="clear_cart")
    builder.adjust(1)
    await message.answer(
        text,
        reply_markup=builder.as_markup()
    )


# /////
@router.callback_query(F.data == "clear_cart")
async def clear_cart(callback: CallbackQuery):
    print("CLEAR WORKS")

    user_id = callback.from_user.id

    if user_id in user_orders:
        user_orders[user_id].clear()

    await callback.message.edit_text("🗑 Корзина очищена.")
    await callback.answer()


# /////
@router.callback_query(F.data == "checkout")
async def checkout(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    if user_id not in user_orders:
        await callback.answer("Корзина пустая.")
        return

    order = user_orders[user_id]

    if not order.get_products():
        await callback.answer("Корзина пустая.")
        return

    telegram_id = callback.from_user.id

    client_id = get_client_id(telegram_id)

    order_id = create_order(client_id)

    for product in order.get_products():
        add_product_to_order(
            order_id,
            product.product_id
        )

    complete_order(order_id)

    order.clear()

    await callback.message.answer("📦 Заказ оформлен!")
    await asyncio.sleep(2)
    await callback.message.answer("🔧 Проверяем товары...")
    await asyncio.sleep(2)
    await callback.message.answer("📦 Упаковываем...")
    await asyncio.sleep(2)
    await callback.message.answer("🚚 Передаем в доставку...")
    await asyncio.sleep(2)
    await callback.message.answer("✅ Заказ готов!")

    await callback.answer()