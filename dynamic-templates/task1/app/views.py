import csv
from django.shortcuts import render
from django.views.generic import TemplateView


class InflationView(TemplateView):
    template_name = 'inflation.html'


    def get(self, request, *args, **kwargs):
        # чтение csv-файла и заполнение контекста
        data = {}

        with open('inflation_russia.csv', newline='', encoding='UTF8') as csvfile:
            reader = list(csv.reader(csvfile, delimiter=','))

            for row_number in range(1, len(reader)):

                year_int_list = []
                year_stat_list = reader[row_number][0].split(';')

                for month in year_stat_list:
                    if month == '':
                        year_int_list.append('-')
                    else:
                        year_int_list.append(float(month))

                data.update({int(year_int_list.pop(0)): year_int_list})

        context = {}
        context['data'] = data
        context['header'] = reader[0][0].split(';')

        return render(request, self.template_name,
                      context)



