from aiogram import Router,F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class Addlesson(StatesGroup):
    name = State()
    age = State()
    phone_number = State()

router_add_name = Router()

@router_add_name.message(Command('name'))
async def add_start_fsm(message: Message, state: FSMContext):
    await message.answer('Введите ваше имя: ')
    await state.set_state(Addlesson.name)

@router_add_name.message(Addlesson.name)
async def add_name(message: Message, state: FSMContext):
    name = message.text
    if name.isdigit():
        await message.answer('Пожалуйста, введите корректное имя.')
        name = None
        await message.answer('Введите ваш имя: ')
        await state.set_state(Addlesson.name)
    else:
        await state.update_data(name=name)
        await state.set_state(Addlesson.age)
        await message.answer('Введите ваш возраст: ')
    

@router_add_name.message(Addlesson.age)
async def add_age(message: Message, state: FSMContext):
    age = message.text
    await state.update_data(age=age)
    await message.answer(f'Ваш возраст: {age}')
    await state.set_state(Addlesson.phone_number)
    await message.answer('Введите ваш номер телефона: ')

@router_add_name.message(Addlesson.phone_number)
async def add_phone_number(message: Message, state: FSMContext):
    phone_number = message.text
    await state.update_data(phone_number=phone_number)
    await message.answer(f'Ваш номер телефона: {phone_number}')
    data = await state.get_data()
    name = data.get('name')
    age = data.get('age')
    phone_number = data.get('phone_number')
    await message.answer(f'Ваши данные:\nИмя: {name}\nВозраст: {age}\nНомер телефона: {phone_number}')


    await state.clear()