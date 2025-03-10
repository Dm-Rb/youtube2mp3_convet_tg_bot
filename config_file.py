import os
from dotenv import load_dotenv


# загружаем переменные окружения из .env
load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")


# екземпляр конфигурации для импорта и использования
config = Config()
