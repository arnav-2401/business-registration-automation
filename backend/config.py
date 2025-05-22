import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_NINJA_KEY = os.getenv("API_NINJA_KEY")
    DB_CONFIG = {
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD")
    }
