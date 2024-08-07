from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import config
import text.admin as admins_text
import bot.keyboards as keyboards
from aiogram.filters import Command
import crud.added_chats as crud_added_chats
from models.added_chats import AddedChats
from models.chats import Chat
import crud.chats as crud_chats
import crud.posts as crud_posts
from models.posts import Posts
from datetime import datetime

router = Router()

@router.message(Command('info'))
async def bot_info(message: Message):
    chat = await crud_added_chats.get_chat_by_title(message.chat.title.lower())
    if not chat:
        return
    await message.answer(
        text=admins_text.send_about,
        reply_markup=keyboards.send_info_about_keyboard(chat.chat_id).as_markup()
    )

    await message.answer(
        text=admins_text.example,
    )

@router.my_chat_member()
async def my_chat_member(message: Message):
    chat_id = message.chat.id
    chat_ = AddedChats(chat_id=chat_id, title=message.chat.title.strip().lower())
    await crud_added_chats.add_new_chat(chat_)


@router.message(lambda msg: msg.chat.type == "group" or msg.chat.type == "supergroup")
async def start_session_in_chat(message: Message):
    chat_id = message.chat.id
    text = message.text
    necessary_chat = await crud_chats.get_chat_by_id(chat_id)
    if necessary_chat is None:
        ...
    else:
        user_id = message.from_user.id

        if '#план' in text.lower():
            post = Posts(
                id=None,
                user_id=user_id,
                chat_id=chat_id,
                time_type='morning',
                sent_time=datetime.now()
            )
            await crud_posts.create_post(post)
        if '#отчёт' in text.lower() or '#отчет' in text.lower():
            post = Posts(
                id=None,
                user_id=user_id,
                chat_id=chat_id,
                time_type='evening',
                sent_time=datetime.now()
            )
            await crud_posts.create_post(post)
