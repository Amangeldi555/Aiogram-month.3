
from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.main_db import add_admin, get_all_drinks, is_admin

from config import ADMIN_SECRET_KEY


router_admin = Router()


# Состояние авторизации администратора
class AdminAuth(StatesGroup):
    waiting_for_key = State()


# Клавиатура администратора
admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔐 Войти как администратор")
        ]
    ],
    resize_keyboard=True
)

admin_panel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Добавить напиток")],
        [KeyboardButton(text="📦 Все напитки")],
        [KeyboardButton(text="✏️ Изменить напиток")],
        [KeyboardButton(text="🗑 Удалить напиток")],
        [KeyboardButton(text="🚪 Выйти из админ-панели")]
    ],
    resize_keyboard=True
)



# Команда /admin
@router_admin.message(Command("admin"))
async def admin_start(message: Message):
    await message.answer(
        "Нажмите кнопку, чтобы войти в панель администратора.",
        reply_markup=admin_keyboard
    )


# Нажатие кнопки авторизации
@router_admin.message(F.text == "🔐 Войти как администратор")
async def admin_login(message: Message, state: FSMContext):
    await state.set_state(AdminAuth.waiting_for_key)

    await message.answer("🔑 Введите секретный ключ администратора:")


# Проверка секретного ключа
@router_admin.message(AdminAuth.waiting_for_key)
async def check_admin_key(message: Message, state: FSMContext):
    if message.text == ADMIN_SECRET_KEY:

        # Сохраняем Telegram ID администратора
        await add_admin(message.from_user.id)

        await state.clear()

        await message.answer(
    "✅ Вы успешно авторизовались как администратор!\n\n"
    "Выберите действие:",
    reply_markup=admin_panel_keyboard
)

    else:
        await message.answer(
            "❌ Неверный секретный ключ. Попробуйте ещё раз."
        )

@router_admin.message(F.text == "📦 Все напитки")
async def admin_all_drinks(message: Message):
    # Проверяем, является ли пользователь администратором
    if not await is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа!")
        return

    drinks = await get_all_drinks()

    if not drinks:
        await message.answer("В базе данных пока нет напитков.")
        return

    text = "📦 Список всех напитков:\n\n"

    for drink in drinks:
        text += (
            f"🆔 ID: {drink['id']}\n"
            f"🥤 Название: {drink['title']}\n"
            f"📂 Тип: {drink['drink_type']}\n"
            f"💰 Цена: {drink['price']} сом\n\n"
        )

    await message.answer(text)