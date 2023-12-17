from aiogram import Bot, Dispatcher
import config
from handlers.admin import router as admin_router
from handlers.chat_messages import router as chat_messages_router
from handlers.userform import router as userform_router


async def main():
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher()
    dp.include_router(admin_router)
    dp.include_router(userform_router)
    dp.include_router(chat_messages_router)
    await dp.start_polling(bot)
