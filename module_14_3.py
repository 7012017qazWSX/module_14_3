from aiogram import Bot, Dispatcher, executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.insert(button)
kb.insert(button2)
kb.insert(button3)

kb_in = InlineKeyboardMarkup(resize_keyboard=True)
button_in = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data="calories")
button_in2 = InlineKeyboardButton(text='Формулы расчёта', callback_data="formulas")
kb_in.insert(button_in)
kb_in.insert(button_in2)


kb_buy = InlineKeyboardMarkup(resize_keyboard=True)
button_buy = InlineKeyboardButton(text='product1', callback_data="product_buying")
button_buy2 = InlineKeyboardButton(text='product2', callback_data="product_buying")
button_buy3 = InlineKeyboardButton(text='product3', callback_data="product_buying")
button_buy4 = InlineKeyboardButton(text='product4', callback_data="product_buying")
kb_buy.insert(button_buy)
kb_buy.insert(button_buy2)
kb_buy.insert(button_buy3)
kb_buy.insert(button_buy4)

s = 0
@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup=kb)


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=kb_in)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("Формула Миффлина-Сан Жеора для мужчин: 10 х вес (кг) + 6,25 x рост (см)"
                              " – 5 х возраст (г) + 5")


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    with open("files/1.png", "rb") as img:
        await message.answer_photo(img, "Название: product1 | Описание: описание1 | Цена: 5000 руб.")
    with open("files/2.png", "rb") as img:
        await message.answer_photo(img, "Название: product2 |"
                                        " Описание: описание2 | Цена: 10000 руб.")
    with open("files/3.png", "rb") as img:
        await message.answer_photo(img, "Название: product3 |"
                                        " Описание:  описание3 | Цена: 15000 руб.")
    with open("files/4.png", "rb") as img:
        await message.answer_photo(img, " Название: product4 |"
                                        " Описание:  описание4 | Цена: 20000 руб.")


    await message.answer("Выберите продукт для покупки:", reply_markup=kb_buy)

@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result_man = int(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    await message.answer(f'Ваша норма калорий {result_man} день')
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
