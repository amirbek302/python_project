# states.py

from aiogram.fsm.state import State, StatesGroup
class ShopState(StatesGroup):
    catalog = State()
    cart = State()
    confirm = State()