from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import config
import text.admin as admins_text
import bot.utils as utils
import bot.keyboards as keyboards

import crud.added_chats as crud_added_chats

from models.chats import Chat
import crud.chats as crud_chats


class SendingNewsletters(StatesGroup):
    sending_newsletter = State()


class AddNewChat(StatesGroup):
    add_new_chat = State()


router = Router()


@router.message(Command('admin'))
async def hello_world(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if chat_id == config.BOT_CHAT_ID:
        if user_id in config.ADMINS:
            await message.answer(
                text=admins_text.welcome_message,
                reply_markup=keyboards.admin_menu
            )
        else:
            await message.answer(f'У вас нет доступа')


@router.callback_query(F.data == 'chat_interactions')
async def chat_interactions(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        text=admins_text.chat_functools,
        reply_markup=keyboards.chat_functools_keyboard.as_markup()
    )


@router.callback_query(F.data == 'add_new_chat')
async def add_new_chat(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        text=admins_text.add_new_chat,
    )
    await state.set_state(AddNewChat.add_new_chat)


@router.message(AddNewChat.add_new_chat)
async def add_new_chat(message: Message, state: FSMContext):
    await state.clear()
    chat_title = message.text.strip().lower()
    chat = await crud_added_chats.get_chat_by_title(chat_title=chat_title)
    if chat is None:
        await message.answer(
            text=admins_text.chat_not_found,
        )
        await state.clear()
    else:
        ...


@router.callback_query(F.data == 'check_chat')
async def check_chat(callback: CallbackQuery):
    ...


@router.callback_query(F.data == 'sending_newsletters')
async def sending_newsletters(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.answer(
        text=admins_text.sent_newsletters,
        reply_markup=keyboards.admin_cancel.as_markup()
    )
    await state.set_state(SendingNewsletters.sending_newsletter)


@router.callback_query(F.data == 'admin_cancel', SendingNewsletters.sending_newsletter)
async def sending_newsletters(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    await callback.message.answer(
        text=admins_text.welcome_message,
        reply_markup=keyboards.admin_menu
    )


@router.message(SendingNewsletters.sending_newsletter)
async def sending_newsletters(message: Message, state: FSMContext):
    await state.clear()

    all_chats = await crud_chats.get_all_chats()
    print(all_chats)
    count = 0
    for i in all_chats:
        chat_id = i['chat_id']
        try:
            await message.copy_to(
                chat_id=chat_id,
            )
            count += 1
        except Exception as e:
            print(e)
    await message.answer(
        text=f'Рассылка отправлена в {count} чат(ов)',
    )
