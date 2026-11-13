
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.main_db import add_user

import inspect

print("ФУНКЦИЯ ADD_USER:", inspect.signature(add_user))
print("ФАЙЛ ADD_USER:", inspect.getfile(add_user))

class AddUser(StatesGroup):
    name = State()
    surname = State()
    age = State()
    phone_number = State()


router_add_user = Router()


# Проверка номера телефона
def validate_phone_number(phone):
    if not phone.isdigit():
        return False

    if len(phone) == 10 and phone.startswith('0'):
        return True

    if len(phone) == 12 and phone.startswith('996'):
        return True

    return False


# Начало регистрации
@router_add_user.message(Command('name'))
async def add_start_fsm(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AddUser.name)

    await message.answer('Введите ваше имя:')


# Получение имени
@router_add_user.message(AddUser.name)
async def add_name(message: Message, state: FSMContext):
    name = message.text or ''

    if not name.strip() or name.isdigit():
        await message.answer('Введите корректное имя!')
        return

    await state.update_data(name=name.strip())
    await state.set_state(AddUser.surname)

    await message.answer('Введите вашу фамилию:')


# Получение фамилии
@router_add_user.message(AddUser.surname)
async def add_surname(message: Message, state: FSMContext):
    surname = message.text or ''

    if not surname.strip() or surname.isdigit():
        await message.answer('Введите корректную фамилию!')
        return

    await state.update_data(surname=surname.strip())
    await state.set_state(AddUser.age)

    await message.answer('Введите ваш возраст:')


# Получение возраста
@router_add_user.message(AddUser.age)
async def add_age(message: Message, state: FSMContext):
    age = message.text or ''

    if not age.isdigit() or not (1 <= int(age) <= 120):
        await message.answer('Введите корректный возраст!')
        return

    await state.update_data(age=int(age))
    await state.set_state(AddUser.phone_number)

    await message.answer(
        'Введите ваш номер телефона:\n'
    )


# Получение телефона и сохранение пользователя
@router_add_user.message(AddUser.phone_number)
async def add_phone_number(message: Message, state: FSMContext):
    phone_number = (message.text or '').replace(' ', '').replace('-', '')

    if not validate_phone_number(phone_number):
        await message.answer(
            'Введите корректный номер телефона!\n'
            'Пример: 996701493636 или 0701493636'
        )
        return

    # Приводим номер к формату +996
    if phone_number.startswith('0'):
        phone_number = '+996' + phone_number[1:]
    else:
        phone_number = '+' + phone_number

    # Получаем все данные из FSM
    data = await state.get_data()

    # Сохраняем в SQLite
    await add_user(
        name=data['name'],
        surname=data['surname'],
        age=data['age'],
        phone_number=phone_number
    )

    await message.answer(
        'Регистрация завершена!\n\n'
        f"Имя: {data['name']}\n"
        f"Фамилия: {data['surname']}\n"
        f"Возраст: {data['age']}\n"
        f"Телефон: {phone_number}"
    )

    await state.clear()
