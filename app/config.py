import os
from dotenv import load_dotenv

"""
Конфиг с загруженными из .env параметрами
"""

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    IMEI_API_TOKEN = os.getenv("IMEI_API_TOKEN", "")
    IMEI_API_URL = os.getenv("IMEI_API_URL", "")
    LOCAL_API_URL = os.getenv("LOCAL_API_URL", "http://localhost:5000/api/check-imei")
    WHITELIST_USERS = list(map(int, os.getenv("WHITELIST_USERS", "").split()))

config = Config()