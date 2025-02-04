from aiogram import Router, types
from aiogram.filters import Command
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker
from datetime import datetime, time
import io
from user.user import user

plot_router = Router()

async def create_daily_plot(logs, daily_target):
    if not logs:
        return None
    
    # Преобразуем время в объекты datetime и сортируем
    times = []
    cumulative = 0
    cumulative_calories = []
    
    # Сортируем записи по времени
    sorted_items = sorted(logs.items(), key=lambda x: x[0])
    
    for time_str, cal in sorted_items:
        times.append(datetime.combine(datetime.today(), time_str))
        cumulative = cal
        cumulative_calories.append(cumulative)
    
    # Создаем график
    plt.figure(figsize=(10, 6))
    
    # Накопленные калории
    plt.plot(times, cumulative_calories, 'o-', label='Накопленние')
    
    # Линия нормы
    plt.axhline(y=daily_target, color='r', linestyle='--', label='Дневная норма')
    
    # Форматирование времени
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    plt.gca().xaxis.set_major_locator(matplotlib.ticker.AutoLocator())
    plt.title('Прогресс за день')
    plt.ylabel('Употреблено')
    plt.xlabel('Время')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    
    # Сохраняем в буфер памяти
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return buf

@plot_router.message(Command("progress_food"))
async def show_daily_progress(message: types.Message):
    data = await user.get_info()
    daily_calories = data['target_calories']
    cal_logs = data['food_logs']
    if not cal_logs:
        await message.answer("Сегодня ещё не было приёмов пищи")
        return
    
    plot_buf = await create_daily_plot(cal_logs, daily_calories)
    total = sum(cal_logs.values())
    
    caption = (
        f"🍎 Прогресс за сегодня:\n"
        f"• Съедено: {total}/{daily_calories} ккал\n"
        f"• Осталось: {daily_calories - total} ккал\n"
    )
    
    await message.answer_photo(
        photo=types.BufferedInputFile(plot_buf.getvalue(), filename="calories.png"),
        caption=caption
    )

@plot_router.message(Command("progress_water"))
async def show_daily_progress(message: types.Message):
    data = await user.get_info()
    daily_water = data['target_water']
    cal_logs = data['water_logs']
    if not cal_logs:
        await message.answer("Сегодня вы ничего не пили")
        return
    
    plot_buf = await create_daily_plot(cal_logs, daily_water)
    total = sum(cal_logs.values())
    
    caption = (
        f"🥤 Прогресс за сегодня:\n"
        f"• Выпито: {total}/{daily_water} ml\n"
        f"• Осталось: {daily_water - total} ml\n"
        f"• Приёмов пищи: {len(cal_logs)}"
    )
    
    await message.answer_photo(
        photo=types.BufferedInputFile(plot_buf.getvalue(), filename="water.png"),
        caption=caption
    )

# Функция для подключения обработчиков
def setup_plot_handlers(dp):
    dp.include_router(plot_router)