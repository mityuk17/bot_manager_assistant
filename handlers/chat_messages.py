from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import config
import text.chat as text_chat
import bot.keyboards as keyboards

router = Router()


@router.message()
async def start_session_in_chat(message: Message):
    necessary_chats = config.NECESSARY_CHATS
    chat_id = message.chat.id
    if chat_id in necessary_chats:
        await message.answer(
            text=text_chat.send_about,
            reply_markup=keyboards.send_info_about_keyboard(message.chat.id).as_markup()
        )

    else:
        print('chat_id не в разрешенных')
