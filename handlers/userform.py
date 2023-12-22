from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import bot.utils as utils
import bot.keyboards as keyboards
import text.userform as text_user_form

from models.users import User as UserDB
import crud.users as crud_users


class RegistrationForm(StatesGroup):
    user_id = State()
    chat_id = State()
    fullname = State()
    town = State()
    time_start = State()
    time_end = State()
    week_days = State()
    job_title = State()
    product = State()
    metrics = State()


class WeekDays(StatesGroup):
    when_working = State()


class AddToDb(StatesGroup):
    done = State()


router = Router()


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    text = message.text
    if not utils.is_user_from_chat(text):
        await message.answer(
            text=text_user_form.wrong_command
        )
    else:
        chat_id_ = text.split(' ')[-1]
        user_id_ = message.from_user.id
        query = await crud_users.get_user_by_user_id_and_chat_id(user_id_, chat_id_)
        if query is not None:
            await message.answer(
                text=text_user_form.already_registered
            )
        else:
            await message.answer(
                text=text_user_form.start_message,
            )
            await message.answer(
                text=text_user_form.full_name,
            )
            await state.update_data(user_id=user_id_, chat_id=chat_id_)
            await state.set_state(RegistrationForm.fullname)


@router.message(RegistrationForm.fullname)
async def full_name(message: Message, state: FSMContext):
    fullname_ = message.text
    if not utils.is_person_fullname(fullname_):
        await message.answer(
            text=text_user_form.wrong_fullname
        )
    else:
        await state.update_data(fullname=fullname_)
        await message.answer(
            text=text_user_form.town,
        )
        await state.set_state(RegistrationForm.town)


@router.message(RegistrationForm.town)
async def town(message: Message, state: FSMContext):
    town_ = message.text
    await state.update_data(town=town_)
    await message.answer(
        text=text_user_form.time_start,
    )
    await state.set_state(RegistrationForm.time_start)


@router.message(RegistrationForm.time_start)
async def time_start(message: Message, state: FSMContext):
    time_start_ = message.text
    if not utils.check_time_format(time_start_):
        await message.answer(
            text=text_user_form.wrong_time_format
        )
    else:
        await state.update_data(time_start=time_start_)
        await message.answer(
            text=text_user_form.time_end,
        )
        await state.set_state(RegistrationForm.time_end)


@router.message(RegistrationForm.time_end)
async def time_end(message: Message, state: FSMContext):
    time_end_ = message.text
    if not utils.check_time_format(time_end_):
        await message.answer(
            text=text_user_form.wrong_time_format
        )
    else:
        await state.update_data(time_end=time_end_)
        await message.answer(
            text=text_user_form.week_days,
            reply_markup=keyboards.week_days_function('default')
        )
        await state.set_state(RegistrationForm.week_days)


@router.callback_query(F.data.startswith('week_day_'), RegistrationForm.week_days)
async def change_days(call: CallbackQuery, state: FSMContext):
    day = str(call.data.split('_')[-1])
    data = await state.get_data()
    days = data.get('week_days')
    if days is None:
        days = ''
    days += day

    await call.message.edit_reply_markup(
        reply_markup=keyboards.week_days_function(days)
    )

    await state.update_data(week_days=days)


@router.callback_query(F.data == 'check_week_days')
async def check_week_days(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    week_days = data.get('week_days')
    if week_days is None:
        await call.message.edit_text(
            text='Ввведите дни работы заново'
        )

        await call.message.answer(
            text='типо заглушка с теми же самыми кнопками. пользователь не выбрал дни работы',
            reply_markup=keyboards.week_days_function('default')
        )

        await call.message.edit_reply_markup()

    else:
        week_days_ = utils.week_days_to_bin(week_days)
        await call.message.edit_reply_markup()
        await call.message.edit_text(
            text=utils.take_days_by_index(week_days_)
        )

        await state.update_data(week_days=week_days_)

        await call.message.answer(
            text=text_user_form.job_title,
        )

        await state.set_state(RegistrationForm.job_title)


@router.message(RegistrationForm.job_title)
async def job_title(message: Message, state: FSMContext):
    job_title_ = message.text
    await state.update_data(job_title=job_title_)
    await message.answer(
        text=text_user_form.product,
    )
    await state.set_state(RegistrationForm.product)


@router.message(RegistrationForm.product)
async def product(message: Message, state: FSMContext):
    product_ = message.text
    await state.update_data(product=product_)
    await message.answer(
        text=text_user_form.metrics,
    )
    await state.set_state(RegistrationForm.metrics)


@router.message(RegistrationForm.metrics)
async def metrics(message: Message, state: FSMContext):
    metrics_ = message.text
    await state.update_data(metrics=metrics_)
    data = await state.get_data()

    user_full_info = utils.user_information(data)
    await message.answer(
        text=user_full_info,
        reply_markup=keyboards.full_information.as_markup()
    )
    await state.clear()

    await state.set_state(AddToDb.done)
    await state.update_data(done=data)


@router.callback_query(F.data == 'not_full_information')
async def full_information(call: CallbackQuery, state: FSMContext):
    await call.answer()

    await state.clear()

    await call.message.answer(
        text=text_user_form.not_logged_in,
    )

    await call.message.edit_reply_markup()


@router.callback_query(F.data == 'full_information')
async def full_information(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    await state.clear()
    user_model = UserDB(**data['done'])
    await crud_users.create_user(user_model)

    await call.message.answer(
        text=text_user_form.logged_in
    )
    await call.message.edit_reply_markup()
