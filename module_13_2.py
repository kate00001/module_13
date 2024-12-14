from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = '8136216087:AAGHp3KvTaGUL5mx444pVs44KS8sE507Y-M'
bot = Bot (token = api)
dp = Dispatcher (bot, storage = MemoryStorage())

@dp.message_handler(commands = ['start'])
async def start(message):
    print('Привет! Я бот помогающий твоему здоровью.')

@dp.message_handler()
async def all_massages(message):
    print('Введите команду /start, чтобы начать общение.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)
