
from aiogram import Bot, Dispatcher
from decouple import config


# Токен Telegram-бота из .env
TOKEN = config("TOKEN")

# Секретный ключ администратора из .env
ADMIN_SECRET_KEY = config("ADMIN_SECRET_KEY")

# Создание бота
bot = Bot(token=TOKEN)

# Создание диспетчера
dp = Dispatcher()

# Путь к базе данных
path_db = "database/drinks.db"
