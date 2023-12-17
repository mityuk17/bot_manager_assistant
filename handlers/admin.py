from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import config
# from models.chats import Chat
# from crud.chats import create_chat

router = Router()


@router.message(Command('admin'))
async def hello_world(message: Message):
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        await message.answer(f'Hello, admin - {message.from_user.first_name}!')
    else:
        await message.answer(f'У вас нет доступа')


# @router.callback_query()
# async def callback_handler(message: Message):
#     text = 'работа'
#     chat = Chat(chat_id=message.chat.id, excluded_users=message.from_)
#     await create_chat(chat)
