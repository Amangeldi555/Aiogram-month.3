from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from config import bot
from datetime import datetime
import random

router_commands = Router()

@router_commands.message(Command('start'))
async def start_handler(message: Message):
    await message.answer('Привет мир!')

    await bot.send_message(chat_id=message.from_user.id, 
                           text=f'Привет! {message.from_user.full_name} \nТвой телеграм ID > {message.from_user.id}')



@router_commands.message(F.text == 'привет')
async def hello_handler(message: Message):
    await message.answer('Салам')


@router_commands.message(Command('sticker'))
async def sticker_handler(message: Message):
    await message.answer_sticker(sticker='CAACAgIAAxkBAAM5auCySPyaBYsHzBJnxxDp79pfm1sAAqirAAKFa_lIF38CcJWB3Wg9BA')
    await message.answer_sticker(sticker='CAACAgIAAxkBAAM1auCx0ITQ88ljCxCaBsYQuKdB2vEAAuMAA1eEbA_LD3f9g8IMvD0E')



@router_commands.message(Command('mem'))
async def mem_handler(message: Message):
    photo = FSInputFile('media/image.png')
    await message.answer_photo(photo=photo)

@router_commands.message(Command('time'))
async def time_handler(message:Message):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    await message.answer(f"Текущее время: {formatted_time}")

@router_commands.message(Command('random'))
async def random_handler(message:Message):
    random_number = random.randint(1, 100)
    await message.answer(f"случайное число: {random_number}")

@router_commands.message(Command('joke'))
async def random_handler(message:Message):
    random_joke = random.choice(['Почему программисты не любят природу\nТам слишком много багов!😂','Ты сделал домашку\nДа, но Python её не понял.🤣','Почему компьютер замёрз?\nПотому что Windows открыты!🥶','Мой будильник настоящий враг\nКаждый день начинает войну!⏰','Доктор, я постоянно разговариваю сам с собой! И что вы думаете по этому поводу?\nНе ваше дело! 😂'])
    await message.answer(f"СЛУЧАЙНАЯ ШУТКА:\n{random_joke}")