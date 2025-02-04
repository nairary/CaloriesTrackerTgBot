from managers.calories_manager import count_callories
from managers.water_manger import count_water
from aiogram import Router, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from middlewares.states import Form
from user.user import user

router = Router()

# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.reply("Добро пожаловать! Я ваш бот.\nВведите /help для списка команд.")

# Обработчик команды /help
@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply(
        "Доступные команды:\n"
        "/start - Начало работы\n"
        "/set_profile - Задать профиль\n"
        "/info - Получить информацию по профилю\n"
        "/log_food <foog>, <grams> - Указать съеденную еду\n"
        "/log_water <ml> - Указать выпитую воду\n"
        "/progress_food - Получить график питания за день\n"
        "/progress_water - Получить график воды за день\n"
        "/log_workout <workout>, <time> - Указать активность\n"
    )

# FSM: диалог с пользователем
@router.message(Command("set_profile"))
async def start_form(message: Message, state: FSMContext):
    await message.reply("Введите ваше имя:")
    await state.set_state(Form.username)

@router.message(Form.username)
async def start_form(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.reply("Введите ваш вес:")
    await state.set_state(Form.weight)

@router.message(Form.weight)
async def start_form(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.reply("Введите ваш рост (в см):")
    await state.set_state(Form.height)

@router.message(Form.height)
async def process_height(message: Message, state: FSMContext):
    await state.update_data(height=message.text)
    await message.reply("Введите ваш возраст:")
    await state.set_state(Form.age)

@router.message(Form.age)
async def process_(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.reply("Сколько минут активности у вас в день?")
    await state.set_state(Form.activity)

@router.message(Form.activity)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(activity=message.text)
    await message.reply("В каком городе вы проживаете? (Английскими буквами)")
    await state.set_state(Form.city)

# Обработчик команды /keyboard с инлайн-кнопками
@router.message(Form.city)
async def show_keyboard(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Да", callback_data="cal_yes")],
            [InlineKeyboardButton(text="Нет", callback_data="cal_no")],
        ]
    )
    await message.reply("Автоматически рассчитать дневную норму калорий?", reply_markup=keyboard)

keyboard_water = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Да", callback_data="yes")],
            [InlineKeyboardButton(text="Нет", callback_data="no")],
        ]
    )

@router.callback_query(lambda c: c.data == "cal_yes")
async def handle_yes(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    calories_count = await count_callories(data)
    print(f"Ваша норма калорий: {calories_count}")
    await state.update_data(target_calories=calories_count)
    
    await callback.message.answer("Автоматически рассчитать дневную норму воды?", reply_markup=keyboard_water)

@router.callback_query(lambda c: c.data == "cal_no")
async def handle_no(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.waiting_for_calories_message)
    await callback.answer()

@router.message(Form.waiting_for_calories_message)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(target_calories=message.text)
    await state.set_state(Form.calories)

@router.callback_query(lambda c: c.data == "yes")
async def handle_yes(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    water_norma, city_temperature = await count_water(data)
    print(f"Ваша норма воды: {water_norma}")
    await state.update_data(temperature=city_temperature)
    await state.update_data(target_water=water_norma)
    await state.set_state(Form.profile_is_set)
    
    data = await state.get_data()
    username = data.get("username")
    weight = data.get("weight")
    height = data.get("height")
    age = data.get("age")
    activity = data.get("activity")
    city = data.get("city")
    target_calories = data.get("target_calories")
    target_water = data.get("target_water")
    
    user.set(username, weight, height, age, activity, city, target_calories, target_water)
    
    await callback.answer(
        text="Настройка профиля закончена, ознакомьтесь с данными при помощи команды /info",
        show_alert=True,
)

@router.callback_query(lambda c: c.data == "no")
async def handle_no(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.waiting_for_water_message)
    await callback.message.answer("Пожалуйста, введите вашу дневную норму воды")
    await callback.answer()

@router.message(Form.waiting_for_water_message)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(target_water=message.text)
    await state.set_state(Form.profile_is_set)

    data = await state.get_data()
    username = data.get("username")
    weight = data.get("weight")
    height = data.get("height")
    age = data.get("age")
    activity = data.get("activity")
    city = data.get("city")
    target_calories = data.get("target_calories")
    target_water = data.get("target_water")
    
    user.set(username, weight, height, age, activity, city, target_calories, target_water)
    show_info(message, state)

@router.message(Command("info"))
async def show_info(message: Message, state: FSMContext):
    data = await state.get_data()
    username = data.get("username")
    weight = data.get("weight")
    height = data.get("height")
    age = data.get("age")
    activity = data.get("activity")
    city = data.get("city")
    target_calories = data.get("target_calories")
    target_water = data.get("target_water")
    message_text = f"Привет, {username}!\nТвой рост: {height}\nТвой вес: {weight}\nТвой возраст: {age} лет\nТвоя активость: {activity} мин/день\nТы живешь в городе: {city}\n\nТвоя дневная норма калорий: {target_calories}!\nТвоя дневная норма воды: {round(target_water, 2)} ml\n"
    
    

    await message.answer(message_text)

# Функция для подключения обработчиков
def setup_profile_handlers(dp):
    dp.include_router(router)