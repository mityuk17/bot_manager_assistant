from datetime import datetime


def check_type(s: str) -> bool:
    if s == '#morning' or s == '#evening':
        return False
    return True


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
