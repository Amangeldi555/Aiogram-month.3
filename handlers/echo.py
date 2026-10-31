from aiogram import F, Router
from aiogram.types import Message


router_echo = Router()


@router_echo.message(F.sticker)
async def get_sticker_id_handler(message: Message):
    await message.answer(f'ID - стикера - {message.sticker.file_id}')


@router_echo.message(F.text)
async def echo_handler(message: Message):
    await message.answer('Такой команды в боте нет!')