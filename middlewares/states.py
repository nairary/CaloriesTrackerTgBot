from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    weight = State()
    height = State()
    age = State()
    activity = State()
    city = State()
    calories = State()
    username = State()
    water = State()
    target_calories = State()
    target_water = State()
    temperature = State()

    waiting_for_calories_message = State()
    waiting_for_water_message = State()

    return_info = State()

    profile_is_set = State()