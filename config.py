
from pathlib import Path

from aiogram import Bot, Dispatcher
from decouple import config

BASE_DIR = Path(__file__).resolve().parent
path_db = str(BASE_DIR / "database" / "drinks.db")

token = config("TOKEN")

bot = Bot(token=token)
dp = Dispatcher()