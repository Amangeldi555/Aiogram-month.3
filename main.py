
import asyncio
import logging

from config import bot, dp
from handlers import (
    commands,
    fsm_add_drink,
    fsm_add_user,
    echo,
    select_all_drinks
)

from database.main_db import init_db, get_users


async def on_startup(bot):
    await init_db()

    users = await get_users()
    print("ВСЕ ПОЛЬЗОВАТЕЛИ:", users)

    await bot.send_message(
        chat_id=5221584049,
        text="Бот успешно запущен!"
    )


# Подключение роутеров
dp.include_router(commands.router_commands)
dp.include_router(fsm_add_drink.router_add_title)
dp.include_router(fsm_add_user.router_add_user)
dp.include_router(select_all_drinks.router_all_drinks)
dp.include_router(echo.router_echo)

dp.startup.register(on_startup)


async def main():
    print("ПОДКЛЮЧЕННЫЕ РОУТЕРЫ:")
    print(dp.sub_routers)

    print("РОУТЕР ПОЛЬЗОВАТЕЛЕЙ:", fsm_add_user.router_add_user)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
