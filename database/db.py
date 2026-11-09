
import aiosqlite
from database.queries import (
    create_drinks,
    drink_details,
    insert_drink,
    insert_drink_details,
    create_users,
    insert_user
)

from config import path_db


async def init_db():
    async with aiosqlite.connect(path_db) as conn:
        await conn.execute("PRAGMA foreign_keys = ON")

        await conn.execute(create_drinks)
        await conn.execute(drink_details)
        await conn.execute(create_users)

        await conn.commit()

        print("База данных успешно создана!")


async def add_drink(title, drink_type, price, description):
    async with aiosqlite.connect(path_db) as conn:
        await conn.execute("PRAGMA foreign_keys = ON")

        cursor = await conn.execute(
            insert_drink,
            (title, drink_type, price)
        )

        drink_id = cursor.lastrowid

        await conn.execute(
            insert_drink_details,
            (description, drink_id)
        )

        await conn.commit()

        print("Напиток успешно добавлен!")




async def add_user(name, age, phone_number):
    print("ШАГ 1: Начинаем сохранение")

    async with aiosqlite.connect(path_db) as conn:
        print("ШАГ 2: Подключились к базе:", path_db)

        await conn.execute(
            insert_user,
            (name, age, phone_number)
        )

        print("ШАГ 3: Выполнили INSERT")

        await conn.commit()

        print("ШАГ 4: Выполнили COMMIT")

    

        

async def get_users():
    async with aiosqlite.connect(path_db) as conn:
        async with conn.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()




