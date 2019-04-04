from django.shortcuts import render
# Create your views here.


def home(request):
    context = {'result': 'РАБОТАЕТ'}
    return render(request, 'app/calc.html', context)
