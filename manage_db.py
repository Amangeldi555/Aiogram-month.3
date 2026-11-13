
import asyncio
import aiosqlite

from config import path_db


# ПОКАЗАТЬ ПОЛЬЗОВАТЕЛЕЙ

async def show_users():
    async with aiosqlite.connect(path_db) as conn:
        async with conn.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()

        for user in users:
            print(user)

# ДОБАВИТЬ ПОЛЬЗОВАТЕЛЯ

async def add_new_user():
    name = input("Имя: ")
    surname = input("Фамилия: ")
    age = int(input("Возраст: "))
    phone = input("Телефон: ")

    async with aiosqlite.connect(path_db) as conn:
        await conn.execute(
            """
            INSERT INTO users (name, surname, age, phone_number)
            VALUES (?, ?, ?, ?)
            """,
            (name, surname, age, phone)
        )
        await conn.commit()

    print("Пользователь добавлен!")

# ИЗМЕНИТЬ ПОЛЬЗОВАТЕЛЯ

async def update_user():
    user_id = int(input("ID пользователя: "))
    new_name = input("Новое имя: ")

    async with aiosqlite.connect(path_db) as conn:
        await conn.execute(
            "UPDATE users SET name = ? WHERE id = ?",
            (new_name, user_id)
        )
        await conn.commit()

    print("Данные пользователя обновлены!")

# УДАЛИТЬ ПОЛЬЗОВАТЕЛЯ

async def delete_user():
    user_id = int(input("ID пользователя для удаления: "))

    async with aiosqlite.connect(path_db) as conn:
        await conn.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )
        await conn.commit()

    print("Пользователь удалён!")

# ПОКАЗАТЕЛЬ НАПИТОВ

async def show_drinks():
    async with aiosqlite.connect(path_db) as conn:
        async with conn.execute(
            """
            SELECT drinks.id, drinks.title, drinks.drink_type,
                   drinks.price, drink_details.description
            FROM drinks
            LEFT JOIN drink_details
            ON drinks.id = drink_details.drink_id
            """
        ) as cursor:
            drinks = await cursor.fetchall()

        for drink in drinks:
            print(drink)


# ДОБАВЛЕНИЕ НАПИТКА
async def add_new_drink():
    title = input("Название напитка: ")
    drink_type = input("Тип напитка: ")
    price = float(input("Цена: "))
    description = input("Описание: ")

    async with aiosqlite.connect(path_db) as conn:
        cursor = await conn.execute(
            """
            INSERT INTO drinks (title, drink_type, price)
            VALUES (?, ?, ?)
            """,
            (title, drink_type, price)
        )

        drink_id = cursor.lastrowid

        await conn.execute(
            """
            INSERT INTO drink_details (description, drink_id)
            VALUES (?, ?)
            """,
            (description, drink_id)
        )

        await conn.commit()

    print("Напиток добавлен!")


# ИЗМЕНИТЬ ЦЕНУ НАПИТКА

async def update_drink():
    drink_id = int(input("ID напитка: "))
    new_price = float(input("Новая цена: "))

    async with aiosqlite.connect(path_db) as conn:
        await conn.execute(
            "UPDATE drinks SET price = ? WHERE id = ?",
            (new_price, drink_id)
        )
        await conn.commit()

    print("Цена обновлена!")

# УДАЛИТЬ НАПИТОК

async def delete_drink():
    drink_id = int(input("ID напитка для удаления: "))

    async with aiosqlite.connect(path_db) as conn:
        await conn.execute(
            "DELETE FROM drink_details WHERE drink_id = ?",
            (drink_id,)
        )

        await conn.execute(
            "DELETE FROM drinks WHERE id = ?",
            (drink_id,)
        )

        await conn.commit()

    print("Напиток удалён!")

# ГЛАВНОЕ МЕНЮ

async def main():
    while True:
        print("\n УПРАВЛЕНИЕ БАЗОЙ")
        print("1. Показать пользователей")
        print("2. Добавить пользователя")
        print("3. Изменить имя пользователя")
        print("4. Удалить пользователя")
        print("5. Показать напитки")
        print("6. Добавить напиток")
        print("7. Изменить цену напитка")
        print("8. Удалить напиток")
        print("0. Выход")

        choice = input("Выбери действие: ")

        if choice == "1":
            await show_users()
        elif choice == "2":
            await add_new_user()
        elif choice == "3":
            await update_user()
        elif choice == "4":
            await delete_user()
        elif choice == "5":
            await show_drinks()
        elif choice == "6":
            await add_new_drink()
        elif choice == "7":
            await update_drink()
        elif choice == "8":
            await delete_drink()
        elif choice == "0":
            print("Выход из программы!")
            break
        else:
            print("Неверный выбор!")


if __name__ == "__main__":
    asyncio.run(main())