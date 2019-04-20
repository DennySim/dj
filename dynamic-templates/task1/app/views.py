import csv
from django.shortcuts import render
from django.views.generic import TemplateView


class InflationView(TemplateView):
    template_name = 'inflation.html'

    def get(self, request, *args, **kwargs):
        # чтение csv-файла и заполнение контекста
        data = []

        with open('inflation_russia.csv', newline='', encoding='UTF8') as csvfile:

            reader = csv.DictReader(csvfile, delimiter=';')
            for year in reader:
                data.append(year)

        context = {}
        context['data'] = data

        return render(request, self.template_name,
                      context)



