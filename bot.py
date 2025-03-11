import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config_file import Config
from handlers import router as router_handlers
from callbacks import router as router_callbacks

# Инициализация бота
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router_handlers)
dp.include_router(router_callbacks)

async def main():
    await bot.set_my_commands([
        BotCommand(command="start", description="Запусціць бота"),
        BotCommand(command="help", description="Што рабіць?"),
    ])
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
