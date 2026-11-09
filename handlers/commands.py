from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from config import bot
from handlers.keyboards import main_keyboard
from handlers.fsm_add_drink import AddDrink

from datetime import datetime
import random

router_commands = Router()


# Главное меню
@router_commands.message(Command('start'))
async def start_handler(message: Message):
    await message.answer(
        f"Привет,{message.from_user.full_name}! 👋\n\n"
        "Добро пожаловать! 😄\n\n"
        "Меня зовут Аман, я разработал этого бота, "
        "чтобы сделать выбор и заказ напитков "
        "максимально удобными для вас. 🥤\n\n"
        "Здесь вы можете посмотреть ассортимент "
        "напитков и ознакомиться с меню.\n\n"
        "Выберите нужный раздел в меню ниже 👇",
        reply_markup=main_keyboard
    )
# Приветствие
@router_commands.message(F.text == 'привет')
async def hello_handler(message: Message):
    await message.answer('Салам')


# Стикеры
@router_commands.message(Command('sticker'))
async def sticker_handler(message: Message):
    await message.answer_sticker(
        sticker='CAACAgIAAxkBAAM5auCySPyaBYsHzBJnxxDp79pfm1sAAqirAAKFa_lIF38CcJWB3Wg9BA'
    )
    await message.answer_sticker(
        sticker='CAACAgIAAxkBAAM1auCx0ITQ88ljCxCaBsYQuKdB2vEAAuMAA1eEbA_LD3f9g8IMvD0E'
    )


# Фотография
@router_commands.message(Command('mem'))
async def mem_handler(message: Message):
    photo = FSInputFile('media/image.png')
    await message.answer_photo(photo=photo)


# Текущее время
@router_commands.message(Command('time'))
async def time_handler(message: Message):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    await message.answer(f"Текущее время: {formatted_time}")


# Случайное число
@router_commands.message(Command('random'))
async def random_handler(message: Message):
    random_number = random.randint(1, 100)
    await message.answer(f"Случайное число: {random_number}")

# Случайная шутка
@router_commands.message(Command('joke'))
async def joke_handler(message: Message):
    random_joke = random.choice([
        'Почему программисты не любят природу?\nТам слишком много багов! 😂',
        'Ты сделал домашку?\nДа, но Python её не понял. 🤣',
        'Почему компьютер замёрз?\nПотому что Windows открыты! 🥶',
        'Мой будильник настоящий враг.\nКаждый день начинает войну! ⏰',
        'Доктор, я постоянно разговариваю сам с собой!\nИ что вы думаете по этому поводу?\nНе ваше дело! 😂'
    ])
    await message.answer(f"СЛУЧАЙНАЯ ШУТКА:\n{random_joke}")


# Кнопка добавления продукта
@router_commands.message(F.text == "Добавить продукт")
async def add_product_handler(message: Message):
    await message.answer("Начинаем добавление продукта! 📦")


# Кнопка добавления напитка
@router_commands.message(F.text == "Добавить напиток")
async def add_drink_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AddDrink.title)

    await message.answer("Введите название напитка: 🥤")


# Кнопка списка напитков
@router_commands.message(F.text == "Список напитков")
async def drinks_list_handler(message: Message):
    await message.answer(
        "🍹 СОКИ И ЛИМОНАДЫ 📋\n"
        "1. Апельсиновый сок\n"
        "2. Яблочный сок\n"
        "3. Ананасовый сок\n"
        "4. Манговый сок\n"
        "5. Клубничный лимонад\n"
        "6. Мятный лимонад\n"
        "7. Лимонад с маракуйей\n"
        "8. Вишнёвый сок"
    )

# Кнопка помощи
@router_commands.message(F.text == "Помощь")
async def help_handler(message: Message):
    await message.answer("Выбери нужную функцию в меню! ℹ️")