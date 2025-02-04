import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEATHER_TOKEN = os.getenv("OPEN_WEATHER_TOKEN")
IAM_TOKEN = os.getenv("YC_IAM_TOKEN")
FOLDER_ID = os.getenv("YC_FOLDER_ID")

API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"