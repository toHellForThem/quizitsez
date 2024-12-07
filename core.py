import logging
import aiosqlite
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

logging.basicConfig(level=logging.INFO)

API_TOKEN = "8067267998:AAHm_KmtvzOW4S4DVSiUzea1NI9Sxp7yvwY"

bot = Bot(token=API_TOKEN)

dp = Dispatcher()

DB_NAME = "quiz_bot.db"

quiz_data = []

with open("data.json", "r", encoding="utf-8") as f:
    quiz_data = list(json.load(f))
