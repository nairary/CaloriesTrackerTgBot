import asyncio
from aiogram import Bot, Dispatcher
from config.config import TOKEN
from handlers.set_profile import setup_profile_handlers
from handlers.get_callories import setup_callories_handlers
from handlers.plot_progress import setup_plot_handlers
from handlers.log_action import setup_workout_handlers
from middlewares.middlewares import LoggingMiddleware


# Создаем экземпляры бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Настраиваем middleware и обработчики
dp.message.middleware(LoggingMiddleware())
setup_profile_handlers(dp)
setup_callories_handlers(dp)
setup_plot_handlers(dp)
setup_workout_handlers(dp)

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())