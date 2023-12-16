from aiogram import Bot, Dispatcher
import config
import handlers.admin as admin_handler


async def main():
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher()
    dp.include_router(admin_handler.router())
    await dp.start_polling(bot)
