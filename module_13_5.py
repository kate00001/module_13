from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, reply_keyboard


api = 'хххххххххххххххххххххххххххххххххххххххххххххххххххххххххх'
bot = Bot (token = api)
dp = Dispatcher (bot, storage = MemoryStorage())

kb = ReplyKeyboardMarkup()
button = KeyboardButton (text = 'Расчитать')
kb.add(button)
button2 = KeyboardButton (text = 'Информация')
kb.add(button2)


@dp.message_handler(commands=['start'])
async def info(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью!', reply_markup = kb)

@dp.message_handler(text = 'Информация')
async def calories(message):
    await message.answer('Я экспериментальный бот, сейчас я могу считать норму твоих калорий,'
                         'а потом еще много чего смогу полезного сделать')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text = 'Расчитать')
async def set_age(message: Message):
    await message.reply("Введите свой возраст:")
    await UserState.age.set()  # Переходим в состояние ожидания возраста


@dp.message_handler(state=UserState.age)
async def set_growth(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = int(message.text)
    await message.reply("Введите свой рост (в см):")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['growth'] = int(message.text)
    await message.reply("Введите свой вес (в кг):")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['weight'] = int(message.text)

        age = data['age']
        growth = data['growth']
        weight = data['weight']

        bmr = 10 * weight + 6.25 * growth - 5 * age - 161  # Для женщин

        await message.reply(f"Ваша норма калорий: {bmr:.2f} ккал в день.")

    await state.finish()

@dp.message_handler()
async def all_massages(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer ('Введите команду /start, чтобы начать общение.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)
