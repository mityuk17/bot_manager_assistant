from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import config
import text.admin as admins_text
import bot.utils as utils
import bot.keyboards as keyboards
from bot.bot import bot
import crud.added_chats as crud_added_chats

from models.chats import Chat
import crud.chats as crud_chats

import crud.users as crud_users

from models.newsletters import Newsletters
import crud.newsletters as crud_newsletters


class SendingNewsletters(StatesGroup):
    sending_newsletter = State()
    time_sent = State()
    weekdays = State()
    done = State()


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
        reply_markup=keyboards.chat_functools_keyboard
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
    added_chats = await crud_added_chats.get_all_chats()
    added_chat = utils.check_is_chat_in_added(chat_title, added_chats)
    if added_chat is None:
        await message.answer(
            text=admins_text.chat_not_found,
        )
        await state.clear()
    else:

        chat_ = Chat(
            chat_id=added_chat.chat_id,
            title=added_chat.title,
        )
        await crud_chats.create_chat(chat_)

        await bot.send_message(
            chat_id=added_chat.chat_id,
            text=admins_text.send_about,
            reply_markup=keyboards.send_info_about_keyboard(added_chat.chat_id).as_markup()
        )

        await message.answer(
            text=admins_text.chat_added,
        )

        await state.clear()


@router.callback_query(F.data == 'check_chat')
async def check_chat(callback: CallbackQuery):
    await callback.answer()
    all_chats = await crud_chats.get_all_chats()
    await callback.message.answer(
        text='Выберите чат',
        reply_markup=keyboards.select_chat(all_chats)
    )

    await callback.message.edit_reply_markup()


@router.callback_query(F.data.startswith('chatID_'))
async def check_chat(callback: CallbackQuery):
    chat_id = callback.data.split("_")[-1]
    await callback.answer()
    all_users = await crud_users.get_all_users()
    users = list()
    for user in all_users:
        chat_user_id = user.chat_id
        if chat_id == chat_user_id:
            users.append(user.fullname)
    await callback.message.answer(
        text='\n'.join(users) if users else 'Пользователей с этого чата не существует',
    )
    await callback.message.edit_reply_markup()


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
    newsletter = message.message_id
    await state.update_data(sending_newsletter=newsletter)
    await message.answer(
        text='Напишите время расслыки формата hh:mm'
    )
    await state.set_state(SendingNewsletters.time_sent)


@router.message(SendingNewsletters.time_sent)
async def sending_newsletters(message: Message, state: FSMContext):
    time = message.text
    if utils.check_time_format(time):
        await state.update_data(time_sent=time)
        await message.answer(
            text='в какие дни делаем рассылку?',
            reply_markup=keyboards.week_days_function('default')
        )

        await state.set_state(SendingNewsletters.weekdays)
    else:
        await message.answer(
            text='Введите время в формате hh:mm',
        )


@router.callback_query(F.data.startswith('week_day_'), SendingNewsletters.weekdays)
async def week_days(call: CallbackQuery, state: FSMContext):
    day = str(call.data.split('_')[-1])
    data = await state.get_data()
    days = data.get('weekdays')
    if days is None:
        days = ''
    days += day

    await call.message.edit_reply_markup(
        reply_markup=keyboards.week_days_function(days)
    )

    await state.update_data(weekdays=days)


@router.callback_query(F.data == 'check_week_days')
async def check_week_days(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    weekdays = data.get('weekdays')
    if weekdays is None:
        await call.message.edit_text(
            text='Ввведите дни работы заново'
        )

        await call.message.answer(
            text='типо заглушка с теми же самыми кнопками. пользователь не выбрал дни работы',
            reply_markup=keyboards.week_days_function('default')
        )

        await call.message.edit_reply_markup()

    else:
        week_days_ = utils.week_days_to_bin(weekdays)
        await call.message.edit_reply_markup()
        await call.message.edit_text(
            text=utils.take_days_by_index(week_days_) + '\nВсе верно?',
            reply_markup=keyboards.admin_yes_or_no.as_markup()
        )

        await state.update_data(weekdays=week_days_)


@router.callback_query(F.data.startswith('week_'))
async def check_week_days(call: CallbackQuery, state: FSMContext):
    selection = str(call.data.split('_')[-1])
    await call.answer()
    if selection == 'yes':
        data = await state.get_data()
        newsletter = Newsletters(
            id=None,
            message_id=data.get('sending_newsletter'),
            user_id=call.from_user.id,
            time=data.get('time_sent'),
            week_days=data.get('weekdays'),
        )
        await crud_newsletters.create_newsletter(newsletter)
        await call.message.answer(
            text='Рассылка успешно отправлена'
        )

    else:
        await call.message.answer(
            text='Отмена действий.'
        )
    await state.clear()
    await call.message.edit_reply_markup()
