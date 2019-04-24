from django import template

register = template.Library()


def get_year(value):

    value = value['Год']
    return value


def get_month_value(month_value):

    if month_value == '':
        color = 'white'
        return color

    month_value = float(month_value)
    if month_value < 0:
        color = 'green'
    elif 1 < month_value < 2:
        color = '#FF7F7F'
    elif 2 <= month_value < 5:
        color = '#FF3333'
    elif month_value > 5:
        color = 'red'
    else:
        color = 'white'

    return color


register.filter('get_year', get_year)
register.filter('get_month_value', get_month_value)
