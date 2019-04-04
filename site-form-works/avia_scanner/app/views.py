import time
import random

from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from django.http import JsonResponse
from django.core.cache import cache

from .models import City
from .forms import SearchTicket


class TicketPageView(FormMixin, TemplateView):
    form_class = SearchTicket
    template_name = 'app/ticket_page.html'


def cities_lookup(request):
    """Ajax request предлагающий города для автоподстановки, возвращает JSON"""

    if 'cities' not in cache:
        cache.set('cities', City.objects.all())

    results = cache.get('cities').filter(name__startswith=request.GET['term'])
    results = [city.name for city in results]

    return JsonResponse(results, safe=False)
