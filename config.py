from aiogram import Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMIN = int(os.getenv('ADMIN'))

bot = Bot(TOKEN, default=DefaultBotProperties(
    parse_mode=ParseMode.HTML))
storage = MemoryStorage()
