import logging
import requests
from config.config import IAM_TOKEN, FOLDER_ID, API_URL

async def get_calories(food: str, grams: int) -> str:
    headers = {
        "Authorization": f"Bearer {IAM_TOKEN}",
        "x-folder-id": FOLDER_ID,
        "Content-Type": "application/json"
    }

    prompt = (
        f"Сколько калорий содержится в {grams} граммах {food}? "
        "Ответ дай ТОЛЬКО в виде числа без каких-либо пояснений, "
        "слов или знаков препинания. Если не знаешь точный ответ, напиши 0."
    )

    data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": 50
        },
        "messages": [{
            "role": "user",
            "text": prompt
        }]
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result['result']['alternatives'][0]['message']['text'].strip()
    
    except Exception as e:
        logging.error(f"Yandex GPT API error: {e}")
        return "error"
    
async def get_workout(workout: str, minutes: float) -> str:
    headers = {
        "Authorization": f"Bearer {IAM_TOKEN}",
        "x-folder-id": FOLDER_ID,
        "Content-Type": "application/json"
    }

    prompt = (
        f"Сколько {workout} сжигает каллорий за {minutes} минут? "
        "Ответ дай ТОЛЬКО в виде числа без каких-либо пояснений, "
        "слов или знаков препинания. Если не знаешь точный ответ, напиши 0."
    )

    data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": 50
        },
        "messages": [{
            "role": "user",
            "text": prompt
        }]
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result['result']['alternatives'][0]['message']['text'].strip()
    
    except Exception as e:
        logging.error(f"Yandex GPT API error: {e}")
        return "error"