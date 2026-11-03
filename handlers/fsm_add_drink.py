
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class AddDrink(StatesGroup):
    title = State()
    type = State()
    price = State()


router_add_title = Router()


@router_add_title.message(Command('add_drink'))
async def add_drink(message: Message, state: FSMContext):
    await message.answer('Введите название напитка:')
    await state.set_state(AddDrink.title)


@router_add_title.message(AddDrink.title)
async def add_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)

    await message.answer('Введите тип напитка:')
    await state.set_state(AddDrink.type)


@router_add_title.message(AddDrink.type)
async def add_type(message: Message, state: FSMContext):
    await state.update_data(type=message.text)

    await message.answer('Введите цену напитка:')
    await state.set_state(AddDrink.price)


@router_add_title.message(AddDrink.price)
async def add_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)

    data = await state.get_data()

    title = data.get('title')
    drink_type = data.get('type')
    price = data.get('price')

    await message.answer(
        f'Название напитка: {title}\n'
        f'Тип напитка: {drink_type}\n'
        f'Цена напитка: {price}'
    )

    await state.clear()