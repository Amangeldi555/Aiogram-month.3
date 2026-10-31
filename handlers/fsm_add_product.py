from aiogram import Router,F
from aiogram.types import Message
from aiogram.filters import command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class AddProduct(StatesGroup):
    name_product = State()
    price = State()
    description = State()

router_add_product = Router()

@router_add_product.massage(command('add_product'))
async def add