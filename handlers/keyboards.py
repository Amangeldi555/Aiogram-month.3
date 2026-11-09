
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить напиток")
        ],


        [
            KeyboardButton(text="Список напитков"),
            KeyboardButton(text="Помощь")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери действие..."
)
