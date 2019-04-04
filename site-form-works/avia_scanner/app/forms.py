from django import forms
from django.forms.widgets import SelectDateWidget

from .widgets import AjaxInputWidget
from .models import City


class SearchTicket(forms.Form):
    city_destination = forms.CharField(widget=AjaxInputWidget('api/city_ajax',
                                          attrs={'class': 'inline right-margin'}),
                                       label='Город назначения')
    city_departure = forms.CharField(label='Город отправления')
    date_departure = forms.DateField(widget=SelectDateWidget(),
                                     label='Дата отправления')




