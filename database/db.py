import sqlite3
from database.queries import CREATE_DRINKS_TABLE


def init_db():
    conn = sqlite3.connect('drinks.db')
    cursor = conn.cursor()

    cursor.execute(CREATE_DRINKS_TABLE)

    conn.commit()
    conn.close()