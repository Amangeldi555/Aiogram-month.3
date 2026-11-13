
import aiosqlite

from database.queries import (
    create_drinks,
    drink_details,
    create_users,
    insert_drink,
    insert_drink_details,
    insert_user,
    select_all_drinks
)

from config import path_db


# Создание таблиц
async def init_db():
    async with aiosqlite.connect(path_db) as conn:
        await conn.execute("PRAGMA foreign_keys = ON")

        await conn.execute(create_drinks)
        await conn.execute(drink_details)
        await conn.execute(create_users)

        # Проверяем столбцы таблицы users
        async with conn.execute("PRAGMA table_info(users)") as cursor:
            columns = await cursor.fetchall()

        column_names = [column[1] for column in columns]

        if "surname" not in column_names:
            await conn.execute(
                "ALTER TABLE users ADD COLUMN surname TEXT NOT NULL DEFAULT ''"
            )

        await conn.commit()

    print("База данных успешно создана!")


# Добавление напитка
async def add_drink(title, drink_type, price):
    async with aiosqlite.connect(path_db) as conn:
        cursor = await conn.execute(
            insert_drink,
            (title, drink_type, price)
        )

        drink_id = cursor.lastrowid

        await conn.commit()

        return drink_id


# Добавление описания напитка
async def add_drink_details(description, drink_id):
    async with aiosqlite.connect(path_db) as conn:
        await conn.execute("PRAGMA foreign_keys = ON")

        await conn.execute(
            insert_drink_details,
            (description, drink_id)
        )

        await conn.commit()


# Получение напитков вместе с описаниями
async def get_all_drinks():
    async with aiosqlite.connect(path_db) as conn:
        conn.row_factory = aiosqlite.Row

        async with conn.execute(select_all_drinks) as cursor:
            return await cursor.fetchall()


# Добавление пользователя
async def add_user(name, surname, age, phone_number):
    async with aiosqlite.connect(path_db) as conn:
        await conn.execute(
            insert_user,
            (name, surname, age, phone_number)
        )

        await conn.commit()

    print("Пользователь успешно добавлен!")


# Получение пользователей
async def get_users():
    async with aiosqlite.connect(path_db) as conn:
        conn.row_factory = aiosqlite.Row

        async with conn.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()