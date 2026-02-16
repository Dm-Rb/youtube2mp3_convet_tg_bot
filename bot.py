from aiogram.types import BotCommand
from config_file import Config
from handlers import router as router_handlers
from callbacks import router as router_callbacks
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer 
import logging
from rm_temp_files import trash_scheduler


logging.basicConfig(
    level=logging.ERROR,  # Только ошибки
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('bot_errors.log', encoding='utf-8'),  # в файл
        # logging.StreamHandler()  # в консоль
    ]
)


# bot init if exist custom Telegram API Server ___
session = AiohttpSession(api=TelegramAPIServer.from_base("http://localhost:8081", is_local=True))
bot = Bot(token=Config.BOT_TOKEN, session=session)
# ___

# default bot init ___
# bot = Bot(token=Config.BOT_TOKEN)
# ___

dp = Dispatcher()
dp.include_router(router_handlers)
dp.include_router(router_callbacks)


async def main():
    await bot.set_my_commands([
        BotCommand(command="start", description="Запусціць бота"),
        BotCommand(command="help", description="Што рабіць?"),
    ])

    asyncio.create_task(trash_scheduler())  # once an hour, it scans the directory with temporary files and deletes
    # those with a date/time older than 1 hour.
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
