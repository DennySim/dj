from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import CalcForm


class CalcView(TemplateView):
    template_name = "app/calc.html"

    def get(self, request):

        form = CalcForm(request.GET)

        if form.is_valid():

            result = round(((int(request.GET.get('initial_fee')) +
                             int(request.GET.get('initial_fee')) *
                             int(request.GET.get('rate'))) /
                            int(request.GET.get('months_count'))), 2)

            common_result = result * int(request.GET.get('months_count'))

            return render(request, self.template_name,
                          {'form': form,
                           'common_result': common_result,
                           'result': result})
        else:
            return render(request, self.template_name, {'form': form})
