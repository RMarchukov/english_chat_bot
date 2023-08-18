import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()

load_dotenv()
TOKEN = os.getenv('TOKEN')
PROXY_URL = os.getenv('PROXY')

bot = Bot(TOKEN, proxy=PROXY_URL)
dp = Dispatcher(bot=bot, storage=storage)
