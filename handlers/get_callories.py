from managers.calories_manager import count_callories
from managers.water_manger import count_water
from aiogram import Router, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from middlewares.states import Form
from api.food_api import get_calories
from user.user import user

log_food_router = Router()

@log_food_router.message(Command("log_food"))
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
        food, grams = command.args.split(",", maxsplit=1)
        grams = float(grams)
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/log_food <food>, <grams>"
        )
        return

    try:
        if grams <= 0:
            raise ValueError

        # Отправка запроса в Yandex GPT
        answer = await get_calories(food, grams)
        
        # Обработка ответа
        if answer == "error":
            raise Exception("API error")
        
        if answer.isdigit():
            calories = int(answer)
            if calories == 0:
                text = "❌ Не удалось определить калорийность для этого блюда"
            else:
                message_date = message.date
                formatted_time = message_date.strftime("%H:%M:%S")

                delta = await user.add_calories(calories, formatted_time)
                if delta < 0:
                    delta_text = f"Вы превысили норму калорий на {abs(delta)} калорий\n"
                else:
                    delta_text = f"Осталось {delta} калорий\n"
                                                
                text = (
                    f"🍽 {food}\n"
                    f"📊 {grams} грамм\n"
                    f"🔥 Калорийность: ~{calories} ккал\n\n"
                    f"✅ Данные добавлены\n"
                    f"{delta_text}"
                )
        else:
            text = "⚠ Не смог распознать ответ. Попробуйте еще раз"

    except ValueError:
        text = "Неправильный формат. Пример:\n/log_food Картофель фри, 200"

    await message.answer(text, parse_mode="HTML")

@log_food_router.message(Command("log_water"))
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
        ml = command.args.split(" ")
        ml = float(ml)
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/log_water <ml>"
        )
        return

    try:
        if ml <= 0:
            raise ValueError

        message_date = message.date
        formatted_time = message_date.strftime("%H:%M:%S")

        delta = await user.add_water(ml, formatted_time)

        if delta < 0:
            delta_text = f"Вы превысили норму воды на {abs(delta)} ml\n"
        else:
            delta_text = f"Осталось выпить {delta} ml\n"

        text = (
            f"🥤 Выпито {ml} воды\n\n"
            f"✅ Данные добавлены\n"
            f"{delta_text}"
        )

    except ValueError:
        text = "Неправильный формат. Пример:\n/log_water 500"

    await message.answer(text, parse_mode="HTML")


def setup_callories_handlers(dp):
    dp.include_router(log_food_router)