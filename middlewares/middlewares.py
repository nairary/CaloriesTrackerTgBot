import logging.handlers
from aiogram import BaseMiddleware
from aiogram.types import Message
import logging

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        socket_handler = logging.handlers.SocketHandler("0.0.0.0", 10000)
        socket_handler.setLevel(logging.INFO)
        
        logger = logging.getLogger("bot")
        logger.setLevel(logging.INFO)
        logger.info(f"Получено сообщение: {event.text}")

        return await handler(event, data)
