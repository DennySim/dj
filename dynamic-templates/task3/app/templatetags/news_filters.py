from django import template
from datetime import datetime

register = template.Library()


@register.filter
def format_date(value):
    delta = round(datetime.now().timestamp() - value, 2)
    if delta < 600:
        return 'только что'
    elif 600 <= delta < 86400:
        return '{} часов назад'.format(int(delta // 3600))
    else:
        return datetime.strftime(datetime.now(), "%Y-%m-%d")


@register.filter
def score(value):

    if int(value) < -5:
        return 'все плохо'
    elif -5 <= int(value) < 5:
        return 'нейтрально'
    else:
        return 'хорошо'


@register.filter
def format_num_comments(value):

    if value == 0:
        return 'Оставьте комментарий'
    elif 0 < value <= 50:
        return value
    else:
        return '50+'


@register.filter
def format_selftext(value, count=5):

    word_list = value.split(' ')

    if len(word_list) > count * 2:
        return ' '.join(word_list[:count]) + ' ... ' + ' '.join(word_list[-count:])
    else:
        return value



