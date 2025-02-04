from managers.calories_manager import count_callories
from managers.water_manger import count_water
from aiogram import Router, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from middlewares.states import Form
from api.food_api import get_workout
from user.user import user

log_workout_router = Router()

@log_workout_router.message(Command("log_workout"))
async def message_handler(
            message: types.Message,
            command: CommandObject
    ):
    if command.args is None:
        await message.anser(
            "Ошибка: не переданы аргументы"
        )
        return
    
    try:
        workout, workout_time = command.args.split(",", maxsplit=1)
        workout_time = float(workout_time)
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/log_workout <workout>, <minutes>"
        )
        return

    try:
        if workout_time <= 0:
            raise ValueError

        # Отправка запроса в Yandex GPT
        answer = await get_workout(workout, workout_time)
        
        # Обработка ответа
        if answer == "error":
            raise Exception("API error")
        
        if answer.isdigit():
            calories = int(answer)
            if calories == 0:
                text = "❌ Не удалось определить сколько калорий сжигает это упражнение"
            else:
                message_date = message.date
                formatted_time = message_date.strftime("%H:%M:%S")

                print(f"{workout_time} % 30 = {workout_time % 30}")
                water_to_drink = 500 * workout_time % 30
                print(f"500 * {workout_time} % 30 = {water_to_drink}")

                await user.remove_calories(calories, formatted_time)
                await user.add_water_for_workout(workout_time, formatted_time)
                                                
                text = (
                    f"🤸🏻‍♂️ {workout} - {workout_time} минут\n\n"
                    f"🔥 Сожгли: ~{calories} ккал\n"
                    f"🚰 Выпейте {water_to_drink} мл воды\n"
                    f"✅ Данные добавлены\n"
                )
        else:
            text = "⚠ Не смог распознать ответ. Попробуйте еще раз"

    except ValueError:
        text = "Неправильный формат. Пример:\n/log_workout <workout>, <minutes>"

    await message.answer(text, parse_mode="HTML")

def setup_workout_handlers(dp):
    dp.include_router(log_workout_router)