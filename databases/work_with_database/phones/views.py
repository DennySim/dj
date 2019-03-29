from django.shortcuts import render
from .models import Phone

context = {}


def show_catalog(request):

    option = request.GET.get('sort')

    if option == 'name':
        queryset = Phone.objects.order_by('name')
    elif option == 'min_price':
        queryset = Phone.objects.order_by('price')
    elif option == 'max_price':
        queryset = Phone.objects.order_by('-price')
    else:
        queryset = Phone.objects.all()

    context['phones'] = queryset

    return render(
        request,
        'catalog.html',
        context
    )


def show_product(request, slug):

    queryset = Phone.objects.filter(slug=slug)
    context['phones'] = queryset

    return render(
        request,
        'product.html',
        context
    )
