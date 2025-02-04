import aiohttp
from multiprocessing import Pool
from config.config import WEATHER_TOKEN

async def get_current_temperature_async(town: str):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={town}&units=metric&appid={WEATHER_TOKEN}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url) as response:
                if response.status != 200:
                    error_message = await response.json()
                    return None
                data = await response.json()
                current_temperature = data['main']['temp']
                return current_temperature
        except aiohttp.ClientError as e:
            return None