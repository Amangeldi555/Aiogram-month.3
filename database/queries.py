
create_drinks = """
CREATE TABLE IF NOT EXISTS drinks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    drink_type TEXT NOT NULL,
    price REAL NOT NULL
);
"""

drink_details = """
CREATE TABLE IF NOT EXISTS drink_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    drink_id INTEGER NOT NULL,
    FOREIGN KEY (drink_id) REFERENCES drinks(id)
);
"""

create_users = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    age INTEGER NOT NULL,
    phone_number TEXT NOT NULL
);
"""

insert_drink = """
INSERT INTO drinks (title, drink_type, price)
VALUES (?, ?, ?);
"""

insert_drink_details = """
INSERT INTO drink_details (description, drink_id)
VALUES (?, ?);
"""

insert_user = """
INSERT INTO users (name, surname, age, phone_number)
VALUES (?, ?, ?, ?);
"""

select_all_drinks = """
SELECT
    drinks.id,
    drinks.title,
    drinks.drink_type,
    drinks.price,
    drink_details.description
FROM drinks
INNER JOIN drink_details
ON drinks.id = drink_details.drink_id;
"""
