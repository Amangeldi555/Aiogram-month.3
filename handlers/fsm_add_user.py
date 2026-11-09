
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.db import add_user


class AddUser(StatesGroup):
    name = State()
    age = State()
    phone_number = State()


router_add_user = Router()


# Валидатор номера телефона
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
    await state.set_state(AddUser.name)
    await message.answer('Введите ваше имя:')


# Получение имени
@router_add_user.message(AddUser.name)
async def add_name(message: Message, state: FSMContext):
    name = message.text

    if not name or not name.strip() or name.isdigit():
        await message.answer('Введите корректное имя!')
        return

    await state.update_data(name=name)
    await state.set_state(AddUser.age)
    await message.answer('Введите ваш возраст:')


# Получение возраста
@router_add_user.message(AddUser.age)
async def add_age(message: Message, state: FSMContext):
    age = message.text

    if not age or not age.isdigit() or not (1 <= int(age) <= 120):
        await message.answer('Введите корректный возраст!')
        return

    await state.update_data(age=int(age))
    await state.set_state(AddUser.phone_number)
    await message.answer('Введите ваш номер телефона:')


# Получение телефона
@router_add_user.message(AddUser.phone_number)
async def add_phone_number(message: Message, state: FSMContext):

    phone_number = message.text or ''

    if not validate_phone_number(phone_number):
        await message.answer(
            "Введите корректный номер телефона!\n"
            "Пример: 996700123456 или 0700123456"
        )
        return
    

    data = await state.get_data()

    if phone_number.startswith('0'):
        phone_number = '996' + phone_number[1:]
    else:
        phone_number = '+' + phone_number 

    data = await state.get_data()

    await add_user(
        name=data['name'],
        age=data['age'],
        phone_number=phone_number
    )

    await message.answer(
        f"Регистрация завершена!\n\n"
        f"Имя: {data['name']}\n"
        f"Возраст: {data['age']}\n"
        f"Телефон: {phone_number}"
    )

    await state.clear()
