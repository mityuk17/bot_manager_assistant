from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import config
import text.chat as text_chat
import bot.keyboards as keyboards
import crud.added_chats as crud_added_chats
from models.added_chats import AddedChats

router = Router()


@router.my_chat_member()
async def my_chat_member(message: Message):
    chat_id = message.chat.id
    chat_ = AddedChats(chat_id=chat_id, title=message.chat.title.strip().lower())
    await crud_added_chats.add_new_chat(chat_)


@router.message()
async def start_session_in_chat(message: Message):
    NECESSARY_CHATS = [-1002025979042]
    necessary_chats = NECESSARY_CHATS
    chat_id = message.chat.id
    if chat_id in necessary_chats:
        await message.answer(
            text=text_chat.send_about,
            reply_markup=keyboards.send_info_about_keyboard(message.chat.id).as_markup()
        )
        ...
    else:
        print('chat_id не в разрешенных')
