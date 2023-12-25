import sys
import logging
import asyncio
from aiogram import Dispatcher
from db.schemas import chats, users, newsletters, posts, added_chats
from handlers.admin import router as admin_router
from handlers.chat_messages import router as chat_messages_router
from handlers.userform import router as user_form_router
from bot.bot import bot
from db.db import create_tables
from models.users import User
from db.schemas.users import User as UserDB
from models.chats import Chat
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import bot.utils as utils


async def main():
    await create_tables()
    dp = Dispatcher()
    dp.include_router(chat_messages_router)
    dp.include_router(admin_router)
    dp.include_router(user_form_router)

    # 3 таска(10мин, рассылка, кто не отправил)
    shed = AsyncIOScheduler()
    shed.add_job(utils.reminder, 'interval', minutes=10)
    shed.add_job(utils.remind_every_ten_minutes, 'interval', minutes=10)
    shed.add_job(utils.send_newsletters, 'interval', minutes=5)
    shed.start()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except Exception as exception:
        print(f'Exit! - {exception}')
