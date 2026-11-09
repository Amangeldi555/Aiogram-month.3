
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import db


class AddDrink(StatesGroup):
    title = State()
    type = State()
    description = State()
    price = State()

router_add_title = Router()


@router_add_title.message(Command("add_drink"))
async def add_drink(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Введите название напитка:")
    await state.set_state(AddDrink.title)


@router_add_title.message(AddDrink.title)
async def add_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)

    await message.answer("Введите тип напитка:")
    await state.set_state(AddDrink.type)


@router_add_title.message(AddDrink.type)
async def add_type(message: Message, state: FSMContext):
    await state.update_data(type=message.text)

    await message.answer("Введите описание напитка:")
    await state.set_state(AddDrink.description)


@router_add_title.message(AddDrink.description)
async def add_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)

    await message.answer("Введите цену напитка:")
    await state.set_state(AddDrink.price)


@router_add_title.message(AddDrink.price)
async def add_price(message: Message, state: FSMContext):
    try:
        price = float(message.text.replace(",", "."))
        if price <= 0:
            raise ValueError
    except (ValueError, TypeError):
        await message.answer("Введите корректную цену числом!")
        return

    data = await state.get_data()

    title = data.get("title")
    drink_type = data.get("type")
    description = data.get("description")

    try:
        await db.add_drink(
            title=title,
            drink_type=drink_type,
            price=price,
            description=description
        )
    except Exception as error:
        print(f"Ошибка сохранения: {error}")
        await message.answer("Не удалось сохранить напиток. Проверьте базу данных.")
        return

    await message.answer(
        f"Напиток успешно сохранён!\n\n"
        f"Название: {title}\n"
        f"Тип: {drink_type}\n"
        f"Описание: {description}\n"
        f"Цена: {price}"
    )

    await state.clear()
