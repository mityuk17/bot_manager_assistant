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


def take_names_by_index(s: str) -> str:
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
