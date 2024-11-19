from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_r = types.KeyboardButton(text='Рассчитать')
button_i = types.KeyboardButton(text='Информация')
kb.add(button_r, button_i)

in_kb = InlineKeyboardMarkup(resize_keyboard=True)
button_menu1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_menu2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
in_kb.row(button_menu1, button_menu2)



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()

@dp.message_handler(commands=['start'])
async def consol_command(messeage):
    await messeage.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Информация о боте!')

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=in_kb)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161 для женщин \n '
                              '10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) + 5 для мужчин')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_gender(message, state):
    await state.update_data(weight=message.text)
    await message.answer('Введите свой пол "м" или "ж"')
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def send_calories(message, state):
    await state.update_data(gender=message.text.lower())
    data = await state.get_data()
    if str(data['gender']) == 'м':
        calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
        await message.answer(f'Ваши калории {calories}')
    elif data['gender'] == 'ж':
        calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
        await message.answer(f'Ваши калории {calories}')
    else:
        await message.answer(f'невозможно высчитать, пол введен не по образцу')
    await state.finish()


@dp.message_handler()
async def other_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
