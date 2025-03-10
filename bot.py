import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from config_file import Config
from dowload_from_youtube import ytd_obj
from handlers import router as router_handlers


# Инициализация бота
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router_handlers)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
