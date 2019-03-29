from django.shortcuts import render

from .models import Phone, SmartPhone, MobilePhone


def show_catalog(request):
    phones = Phone.objects.all()

    context = {}
    context['phones'] = [{'id': '№', 'price': 'Цена', 'brand': 'Производитель',
                          'model': 'Модель', 'color': 'Цвет',
                          'operating_system': 'ОС',
                          'screen_matrix': 'Матрица', 'cpu': 'Процессор',
                          'ram': 'Память', 'fm_radio': 'Радио',
                          'torch': 'Фонарь'}]

    for phone in phones:

        phone_params = {}
        phone_params['id'] = phone.id
        phone_params['price'] = phone.price
        phone_params['brand'] = phone.brand
        phone_params['model'] = phone.model
        phone_params['color'] = phone.color
        smart_func = SmartPhone.objects.get(id=phone.id)
        phone_params['operating_system'] = smart_func.operating_system
        phone_params['screen_matrix'] = smart_func.screen_matrix
        phone_params['cpu'] = smart_func.cpu
        phone_params['ram'] = smart_func.ram
        old_func = MobilePhone.objects.get(id=phone.id)
        phone_params['fm_radio'] = old_func.fm_radio
        phone_params['torch'] = old_func.torch

        context['phones'].append(phone_params)

    return render(
        request,
        'catalog.html',
        context
    )
