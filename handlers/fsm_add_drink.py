
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.main_db import (
    get_all_drinks,
    add_drink,
    add_drink_details
)


class AddDrink(StatesGroup):
    title = State()
    type = State()
    description = State()
    price = State()


router_add_title = Router()


# Показать все напитки
@router_add_title.message(Command("drinks"))
async def show_all_drinks(message: Message):

    drinks = await get_all_drinks()

    if not drinks:
        await message.answer("В базе данных пока нет напитков.")
        return

    text = "Список всех напитков:\n\n"

    for drink in drinks:
        text += (
            f"ID: {drink['id']}\n"
            f"Название: {drink['title']}\n"
            f"Тип: {drink['drink_type']}\n"
            f"Описание: {drink['description']}\n"
            f"Цена: {drink['price']} сом\n"
            f"━━━━━━━━━━━━━━\n"
        )

    await message.answer(text)


# Начало добавления напитка
@router_add_title.message(Command("add_drink"))
async def start_add_drink(message: Message, state: FSMContext):
    await state.clear()

    await message.answer("Введите название напитка:")
    await state.set_state(AddDrink.title)


# Название
@router_add_title.message(AddDrink.title)
async def add_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)

    await message.answer("Введите тип напитка:")
    await state.set_state(AddDrink.type)


# Тип
@router_add_title.message(AddDrink.type)
async def add_type(message: Message, state: FSMContext):
    await state.update_data(type=message.text)

    await message.answer("Введите описание напитка:")
    await state.set_state(AddDrink.description)


# Описание
@router_add_title.message(AddDrink.description)
async def add_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)

    await message.answer("Введите цену напитка:")
    await state.set_state(AddDrink.price)


# Цена и сохранение в две таблицы
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

    title = data["title"]
    drink_type = data["type"]
    description = data["description"]

    try:
        # Сохраняем напиток в первую таблицу
        drink_id = await add_drink(
            title=title,
            drink_type=drink_type,
            price=price
        )

        # Сохраняем описание во вторую таблицу
        await add_drink_details(
            description=description,
            drink_id=drink_id
        )

    except Exception as error:
        print(f"Ошибка сохранения: {error}")

        await message.answer(
            "Не удалось сохранить напиток. Проверьте базу данных."
        )
        return

    await message.answer(
        f"Напиток успешно сохранён!\n\n"
        f"Название: {title}\n"
        f"Тип: {drink_type}\n"
        f"Описание: {description}\n"
        f"Цена: {price} сом\n"
        f"ID напитка: {drink_id}"
    )

    await state.clear()
