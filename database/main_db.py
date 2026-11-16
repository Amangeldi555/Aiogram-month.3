
import aiosqlite

from database.queries import (
    create_drinks,
    drink_details,
    create_users,
    insert_drink,
    insert_drink_details,
    insert_user,
    select_all_drinks,
    delete_drink,
    delete_drink_details
)

from config import path_db


# Создание таблиц
async def init_db():
    async with aiosqlite.connect(path_db) as conn:
        await conn.execute("PRAGMA foreign_keys = ON")

        await conn.execute(create_drinks)
        await conn.execute(drink_details)
        await conn.execute(create_users)
        await conn.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE NOT NULL
    )
""")

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
import os

async def get_all_drinks():
    print("ПУТЬ К БАЗЕ:", os.path.abspath(path_db))

    async with aiosqlite.connect(path_db) as conn:
        conn.row_factory = aiosqlite.Row

        async with conn.execute("SELECT COUNT(*) FROM drinks") as cursor:
            drinks_count = await cursor.fetchone()

        print("КОЛИЧЕСТВО НАПИТКОВ:", drinks_count[0])

        async with conn.execute(select_all_drinks) as cursor:
            drinks = await cursor.fetchall()

        print("НАЙДЕННЫЕ НАПИТКИ:", len(drinks))

        return drinks


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

async def add_admin(telegram_id):
    async with aiosqlite.connect(path_db) as conn:
        await conn.execute(
            "INSERT OR IGNORE INTO admins (telegram_id) VALUES (?)",
            (telegram_id,)
        )
        await conn.commit()

async def is_admin(telegram_id):
    async with aiosqlite.connect(path_db) as conn:
        async with conn.execute(
            "SELECT 1 FROM admins WHERE telegram_id = ?",
            (telegram_id,)
        ) as cursor:
            result = await cursor.fetchone()

            return result is not None

async def remove_drink(drink_id):
    async with aiosqlite.connect(path_db) as conn:
        await conn.execute("PRAGMA foreign_keys = ON")

        await conn.execute(delete_drink_details, (drink_id,))
        await conn.execute(delete_drink, (drink_id,))

        await conn.commit()

        return True