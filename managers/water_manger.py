from api.weather_api import get_current_temperature_async
async def count_water(data):
    user_weight = data.get("weight")
    user_activity = data.get("activity")
    user_city = data.get("city")
    
    user_city_temperature = await get_current_temperature_async(user_city)
    print(f"Температура в вашем городе: {user_city_temperature}")

    water_norma = float(user_weight) * 30. + 500. * float(user_activity) / 30.
    if not user_city_temperature is None:
        if user_city_temperature > 25:
            water_norma += 750 * (user_city_temperature - 25)
    
    return round(water_norma, 2), user_city_temperature