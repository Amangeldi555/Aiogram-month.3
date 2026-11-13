
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database.main_db import get_all_drinks


router_all_drinks = Router()


@router_all_drinks.message(Command("drinks"))
async def show_all_drinks(message: Message):
    drinks = await get_all_drinks()

    if not drinks:
        await message.answer("В базе пока нет связанных напитков.")
        return

    for drink in drinks:
        await message.answer(
            f" ID: {drink[0]}\n"
            f"Название: {drink[1]}\n"
            f"Тип: {drink[2]}\n"
            f"Цена: {drink[3]} сом\n"
            f"Описание: {drink[4]}"
        )
