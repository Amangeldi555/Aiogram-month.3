from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.main_db import remove_drink, is_admin


router_delete = Router()


class DeleteDrink(StatesGroup):
    waiting_for_id = State()
    confirm_delete = State()


# Нажатие на кнопку удаления под карточкой
@router_delete.callback_query(F.data.startswith("delete_drink:"))
async def start_delete_drink(callback: CallbackQuery, state: FSMContext):

    if not await is_admin(callback.from_user.id):
        await callback.answer("У вас нет доступа!", show_alert=True)
        return

    drink_id = int(callback.data.split(":")[1])

    await state.update_data(drink_id=drink_id)
    await state.set_state(DeleteDrink.confirm_delete)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Да, удалить",
                    callback_data="confirm_delete_yes"
                ),
                InlineKeyboardButton(
                    text="❌ Отмена",
                    callback_data="confirm_delete_no"
                )
            ]
        ]
    )

    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer("Подтвердите удаление")


# Подтверждение удаления
@router_delete.callback_query(
    F.data.in_(["confirm_delete_yes", "confirm_delete_no"]),
    DeleteDrink.confirm_delete
)
async def confirm_delete_drink(
    callback: CallbackQuery,
    state: FSMContext
):

    if not await is_admin(callback.from_user.id):
        await callback.answer("У вас нет доступа!", show_alert=True)
        await state.clear()
        return

    if callback.data == "confirm_delete_no":
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer("Удаление отменено")
        await state.clear()
        return

    data = await state.get_data()
    drink_id = data["drink_id"]

    await remove_drink(drink_id)

    await callback.message.edit_text(
        f"🗑 Напиток с ID {drink_id} удалён!"
    )

    await callback.answer("Напиток удалён")
    await state.clear()