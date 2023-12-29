from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models.chats import Chat
import crud.newsletters as crud_newsletters


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


def chat_week_days_function(s: str):
    week_days = [
        [
            InlineKeyboardButton(text='Понедельник ❌', callback_data='chat_week_day_1'),
        ],
        [
            InlineKeyboardButton(text='Вторник ❌', callback_data='chat_week_day_2'),
        ],
        [
            InlineKeyboardButton(text='Среда ❌', callback_data='chat_week_day_3'),
        ],
        [
            InlineKeyboardButton(text='Четверг ❌', callback_data='chat_week_day_4'),
        ],
        [
            InlineKeyboardButton(text='Пятница ❌', callback_data='chat_week_day_5'),
        ],
        [
            InlineKeyboardButton(text='Суббота ❌', callback_data='chat_week_day_6'),
        ],
        [
            InlineKeyboardButton(text='Воскресенье ❌', callback_data='chat_week_day_7'),
        ],
        [
            InlineKeyboardButton(text='ПОДТВЕРДИТЬ', callback_data='check_chat_week_days')
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


def select_chat(chats: list[Chat]):
    keyboard = []
    for chat in chats:
        button = InlineKeyboardButton(text=chat.title, callback_data=f'chatID_{chat.chat_id}')
        keyboard.append([button])
    keyboard.append([
            InlineKeyboardButton(text='Назад', callback_data='chat_interactions'),
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


full_information = InlineKeyboardBuilder()
full_information.add(InlineKeyboardButton(text='Все верно!', callback_data='full_information'))
full_information.add(InlineKeyboardButton(text='Я ошибся!', callback_data='not_full_information'))

admin_selection = [
    [
        InlineKeyboardButton(text='Чаты', callback_data='chat_interactions'),
    ],
    [
        InlineKeyboardButton(text='Рассылки', callback_data='newsletter_information'),
    ]
]
admin_menu = InlineKeyboardMarkup(inline_keyboard=admin_selection)
admin_cancel = InlineKeyboardBuilder()
admin_cancel.add(InlineKeyboardButton(text='Назад', callback_data='newsletter_information'))
admin_newsletter = InlineKeyboardBuilder()
admin_newsletter.add(InlineKeyboardButton(text='Добавить', callback_data='sending_newsletters'))
admin_newsletter.add(InlineKeyboardButton(text='Удалить', callback_data='admin_delete_newsletter'))
admin_newsletter.add(InlineKeyboardButton(text='Посмотреть', callback_data='admin_watch_newsletter'))
admin_newsletter.add(InlineKeyboardButton(text='Назад', callback_data='admin_cancel_to_menu'))

chat_functools = [
    [
        InlineKeyboardButton(text='Добавить чат', callback_data='add_new_chat'),
    ],
    [
        InlineKeyboardButton(text='Подключенные чаты', callback_data='check_chat')
    ],
    [
        InlineKeyboardButton(text='Назад', callback_data='admin_cancel_to_menu'),
    ]
]

back_to_chat_interactions = InlineKeyboardBuilder()
back_to_chat_interactions.add(InlineKeyboardButton(text='Назад', callback_data='chat_interactions'))

chat_functools_keyboard = InlineKeyboardMarkup(inline_keyboard=chat_functools)

admin_yes_or_no = InlineKeyboardBuilder()
admin_yes_or_no.add(InlineKeyboardButton(text='Да', callback_data='week_yes'))
admin_yes_or_no.add(InlineKeyboardButton(text='Нет', callback_data='week_no'))


async def all_newsletters_delete():
    keyboard = []
    newsletters = await crud_newsletters.get_all_newsletters()
    for newsletter in newsletters:
        newsletter_id = newsletter.id
        newsletter_time = newsletter.time.strftime('%H:%M')
        keyboard.append([
            InlineKeyboardButton(text=f'#{newsletter_id} {newsletter_time}',
                                 callback_data=f'newsletter_delete_id_{newsletter_id}'),
        ])
    keyboard.append([
            InlineKeyboardButton(text='Назад', callback_data='newsletter_information'),
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def all_newsletters_check():
    keyboard = [

    ]
    newsletters = await crud_newsletters.get_all_newsletters()
    for newsletter in newsletters:
        newsletter_id = newsletter.id
        newsletter_time = newsletter.time.strftime('%H:%M')
        keyboard.append([
            InlineKeyboardButton(text=f'#{newsletter_id} {newsletter_time}',
                                 callback_data=f'newsletter_check_id_{newsletter_id}'),
        ])
    keyboard.append([
            InlineKeyboardButton(text='Назад', callback_data='newsletter_information'),
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
