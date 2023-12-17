from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def send_info_about_keyboard(chat_id: int | str):
    send_info_about = InlineKeyboardBuilder()
    send_info_about.add(
        InlineKeyboardButton(text='Отправить информацию о себе',
                             url=f'https://t.me/nimble_bar_bot?start={chat_id}')
    )
    return send_info_about


def week_days_function(s: str):
    week_days = [
        [
            InlineKeyboardButton(text='Понедельник ❌', callback_data='week_day_1'),
        ],
        [
            InlineKeyboardButton(text='Вторник ❌', callback_data='week_day_2'),
        ],
        [
            InlineKeyboardButton(text='Среда ❌', callback_data='week_day_3'),
        ],
        [
            InlineKeyboardButton(text='Четверг ❌', callback_data='week_day_4'),
        ],
        [
            InlineKeyboardButton(text='Пятница ❌', callback_data='week_day_5'),
        ],
        [
            InlineKeyboardButton(text='Суббота ❌', callback_data='week_day_6'),
        ],
        [
            InlineKeyboardButton(text='Воскресенье ❌', callback_data='week_day_7'),
        ],
        [
            InlineKeyboardButton(text='ПОДТВЕРДИТЬ', callback_data='check_week_days')
        ]
    ]
    if s != 'default':
        lst = set(list(map(int, list(s))))
        for i in lst:
            text = week_days[i - 1][0].text
            callback_data = week_days[i - 1][0].callback_data
            text = text[:-1] + '✅'
            week_days[i - 1] = [InlineKeyboardButton(text=text, callback_data=callback_data)]
    keyboard = InlineKeyboardMarkup(inline_keyboard=week_days)
    return keyboard


full_information = InlineKeyboardBuilder()
full_information.add(InlineKeyboardButton(text='Все верно!', callback_data='full_information'))
full_information.add(InlineKeyboardButton(text='Я ошибся!', callback_data='not_full_information'))
