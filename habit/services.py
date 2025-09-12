import os

import requests
from dotenv import load_dotenv

from config.settings import TELEGRAM_URL

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


def send_telegram_message(chat_id, text):
    payload = {"chat_id": chat_id, "text": text}
    response = requests.get(f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", data=payload)
    return response.json()
