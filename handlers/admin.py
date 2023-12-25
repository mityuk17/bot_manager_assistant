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
async def admin_menu(message: Message):
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        await message.answer(
            text=admins_text.welcome_message,
            reply_markup=keyboards.admin_menu
        )
    else:
        await message.answer(f'У вас нет доступа к данному функционалу!')


@router.callback_query(F.data == 'chat_interactions')
async def chat_interactions(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        text=admins_text.chat_functools,
        reply_markup=keyboards.chat_functools_keyboard
    )


@router.callback_query(F.data == 'add_new_chat')
async def add_new_chat(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        text=admins_text.add_new_chat,
        reply_markup=None
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

        await bot.send_message(
            chat_id=added_chat.chat_id,
            text=admins_text.example,
        )

        await message.answer(text=admins_text.chat_added)

    await state.clear()


@router.callback_query(F.data == 'check_chat')
async def check_chat(callback: CallbackQuery):
    await callback.answer()
    all_chats = await crud_chats.get_all_chats()
    await callback.message.edit_text(
        text='Выберите подключенный чат:',
        reply_markup=keyboards.select_chat(all_chats)
    )


@router.callback_query(F.data.startswith('chatID_'))
async def check_chat(callback: CallbackQuery):
    await callback.answer()
    chat_id = int(callback.data.split("_")[-1])
    all_users = await crud_users.get_all_users()
    users = list()
    for user in all_users:
        chat_user_id = user.chat_id
        if chat_id == chat_user_id:
            users.append(await utils.get_user_statistic(user))
    await callback.message.edit_text(
        text='\n'.join(users) if users else 'В данном чате отсутствуют пользователи, заполнившие анкету',
        reply_markup=None
    )


@router.callback_query(F.data == 'newsletter_information')
async def sending_newsletters(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        text=admins_text.newsletters_information,
        reply_markup=keyboards.admin_newsletter.as_markup()
    )
    await callback.message.edit_reply_markup()


@router.callback_query(F.data == 'sending_newsletters')
async def sending_newsletters(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text(
        text=admins_text.sent_newsletters,
        reply_markup=keyboards.admin_cancel.as_markup()
    )
    await state.set_state(SendingNewsletters.sending_newsletter)


@router.callback_query(F.data == 'admin_delete_newsletter')
async def admin_delete_newsletter(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        text=admins_text.all_newslers,
        reply_markup=await keyboards.all_newsletters_delete()
    )


@router.callback_query(F.data.startswith('newsletter_delete_id_'))
async def admin_delete_newsletter(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup()
    await crud_newsletters.delete_newsletter(int(callback.data.split("_")[-1]))
    await callback.message.edit_text(
        text='Рассылка успешно удалена!'
    )


@router.callback_query(F.data == 'admin_watch_newsletter')
async def admin_watch_newsletter(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        text=admins_text.watch_newsletter,
        reply_markup=await keyboards.all_newsletters_check()
    )


@router.callback_query(F.data.startswith('newsletter_check_id_'))
async def admin_delete_newsletter(callback: CallbackQuery):
    await callback.answer()

    our_bot_chat = callback.message.chat.id
    newsletter_id = int(callback.data.split("_")[-1])
    newsletter_ = await crud_newsletters.get_newsletter_by_id(newsletter_id)
    newsletter_time = newsletter_.time.strftime('%H:%M')
    text = '''Информация о рассылке:\n'''
    text += f'''Время: {newsletter_time}\n'''
    text += f'''{utils.take_days_by_index(newsletter_.week_days)}'''
    text += f'''Сообщение рассылки:'''
    await callback.message.edit_text(
        text=text,
        reply_markup=None
    )

    await bot.copy_message(
        chat_id=our_bot_chat,
        from_chat_id=newsletter_.user_id,
        message_id=newsletter_.message_id
    )



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
        text='Введите время по МСК, в которое будет проводиться рассылка в формате hh:mm'
    )
    await state.set_state(SendingNewsletters.time_sent)


@router.message(SendingNewsletters.time_sent)
async def sending_newsletters(message: Message, state: FSMContext):
    time = message.text
    if utils.check_time_format(time):
        await state.update_data(time_sent=time)
        await message.answer(
            text='В какие дни должна проводиться рассылка?',
            reply_markup=keyboards.chat_week_days_function('default')
        )
        await state.set_state(SendingNewsletters.weekdays)
    else:
        await message.answer(
            text='Введите время по МСК, в которое будет проводиться рассылка в формате hh:mm',
        )


@router.callback_query(F.data.startswith('chat_week_day_'), SendingNewsletters.weekdays)
async def chat_week_days(call: CallbackQuery, state: FSMContext):
    day = str(call.data.split('_')[-1])
    data = await state.get_data()
    days = data.get('chat_weekdays')
    if days is None:
        days = ''
    days += day

    await call.message.edit_reply_markup(
        reply_markup=keyboards.chat_week_days_function(days)
    )

    await state.update_data(chat_weekdays=days)


@router.callback_query(F.data == 'check_chat_week_days')
async def check_week_days(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    weekdays = data.get('chat_weekdays')
    if weekdays is None:
        await call.message.edit_text(
            text='Не были выбраны дни проведения рассылки, пожалуйста, выберите заново',
            reply_markup=None
        )

        await call.message.answer(
            text='Выберите дни проведения рассылки:',
            reply_markup=keyboards.chat_week_days_function('default')
        )

    else:
        week_days_ = utils.week_days_to_bin(weekdays)
        await call.message.edit_reply_markup()
        await call.message.edit_text(
            text=utils.take_days_by_index(week_days_) + 'Всё верно?',
            reply_markup=keyboards.admin_yes_or_no.as_markup()
        )

        await state.update_data(weekdays=week_days_)


@router.callback_query(F.data == 'week_yes' or F.data == "week_no")
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
        await call.message.edit_text(
            text='Рассылка успешно создана',
            reply_markup=None
        )

    else:
        await call.message.edit_text(
            text='Создание рассылки отменено',
            reply_markup=None
        )
    await state.clear()
