from datetime import datetime, timedelta, time
from models.added_chats import AddedChats
from models.chats import Chat
import crud.chats as crud_chats
import crud.posts as crud_posts
from bot import bot
import crud.users as crud_users
import crud.newsletters as crud_newsletters


def week_days_to_bin(s: str) -> str:
    days = list(set(list(s)))
    days.sort()
    answer = ['0'] * 7
    for i in days:
        answer[int(i) - 1] = '1'
    answer = ''.join(answer)
    return answer


def take_days_by_index(s: str) -> str:
    days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    user_full_info = ''
    working_days = 'Вы работаете по такому графику:\n'
    for i in range(7):
        if s[i] == '1':
            working_days += f'{days[i]}, '
    user_full_info += working_days[:-2] + '\n'
    return user_full_info


def check_time_format(s: str) -> bool:
    try:
        datetime.strptime(s, '%H:%M')
    except ValueError:
        return False
    return True


def is_user_from_chat(s: str) -> bool:
    if len(s.split()) != 2:
        return False
    return True


def is_person_fullname(s: str) -> bool:
    if len(s.split()) != 2:
        return False
    return True


def user_information(data: dict) -> str:
    fullname = data.get('fullname')
    town = data.get('town')
    time_start = data.get('time_start')
    time_end = data.get('time_end')
    week_days = data.get('week_days')
    week_days = take_days_by_index(week_days)
    job_title = data.get('job_title')
    product = data.get('product')
    metrics = data.get('metrics')
    user_full_info = f'Ваше ФИО: {fullname}\nВаш город: {town}\nВремя начала работы: {time_start}\nВремя окончания работы: {time_end}\n'
    user_full_info += week_days
    user_full_info += f'Ваша должность: {job_title}\nВаш продукт: {product}\nПоказатели оценки: {metrics}'
    return user_full_info


def check_is_chat_in_added(chat_title: str, chats: list[AddedChats]) -> AddedChats | None:
    for chat in chats:
        title = chat.title
        if chat_title == title:
            return AddedChats.model_validate(chat, from_attributes=True)
    return None


async def reminder():
    now = datetime.now().time()
    all_chats = await crud_chats.get_all_chats()
    for chat in all_chats:
        morning = list()
        evening = list()
        chat_id = chat.chat_id
        users = await crud_chats.get_users_by_chat_id(chat_id)
        for user in users:
            time_start = user.time_start
            time_end = user.time_end
            if not crud_posts.check_send_information(user.user_id, user.chat_id, 'morning') and time_start < now:
                morning.append(str(user.user_id))
            if not crud_posts.check_send_information(user.user_id, user.chat_id, 'evening') and time_end < now:
                evening.append(str(user.user_id))
        if morning:
            s1 = f'''В данном чате еще не отправили рассылку до начала работы {len(morning)} пользователей:\n{' '.join(morning)}'''
            await bot.send_message(chat_id=chat_id, text=s1)
        if evening:
            s2 = f'''В данном чате еще не отправили рассылку перед завершением работы {len(evening)} пользователей:\n{' '.join(evening)}'''
            await bot.send_message(chat_id=chat_id, text=s2)

        # отправка в чат сообщение прям здесь(с утра ещё не отправили, ещё не отправили вечером)


# вторая функция на 10 минут перед началом и перед концом (чекает каждые 10 минут)
async def remind_every_ten_minutes():
    time_now = datetime.now()
    users = await crud_users.get_all_users()
    today_day = int(datetime.today().weekday())
    for user in users:
        time_start = user.time_start
        time_end = user.time_end
        chat_id = user.chat_id
        week_days = user.week_days
        if time_start - timedelta(minutes=10) <= time_now <= time_start and week_days[today_day - 1] == '1':
            await bot.send_message(chat_id=chat_id,
                                   text=f'{user.fullname}, через 10 минут у вас начинается рабочий день')
        if time_end - timedelta(minutes=10) <= time_now <= time_end and week_days[today_day - 1] == '1':
            await bot.send_message(chat_id=chat_id,
                                   text=f'{user.fullname}, через 10 минут у вас заканчивается рабочий день')


async def send_newsletters():
    time_now = datetime.now().time()
    today_day = int(datetime.today().weekday())
    all_newsletters = await crud_newsletters.get_all_newsletters()
    for newsletter in all_newsletters:
        newsletter_time = newsletter.time
        week_days = newsletter.week_days
        if week_days[today_day - 1] == '1' and newsletter_time - timedelta(minutes=5) <= time_now <= newsletter_time:
            await bot.copy_message(
                chat_id=newsletter.chat_id,
                message_id=newsletter.message_id,
            )

