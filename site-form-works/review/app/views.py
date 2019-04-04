from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from .models import Product, Review
from .forms import ReviewForm


class ProductsList(ListView):
    model = Product
    context_object_name = 'product_list'


class ProductView(DetailView):
    model = Review
    template_name = 'app/product_detail.html'

    def get(self, request, *args, **kwargs):
        context = {}
        form = ReviewForm()
        product_id = Product.objects.get(id=kwargs['pk'])

        context['object'] = product_id
        reviews = Review.objects.filter(product=product_id)
        if reviews:
            context['reviews'] = reviews

        if 'reviewed_products' not in request.session:
            request.session['reviewed_products'] = []

        if product_id.id not in request.session['reviewed_products']:
            # Show "CommentForm" for user who hasn't left a comment yet
            context['form'] = form
        return render(request, 'app/product_detail.html', context)


    def post(self, request, **kwargs):

        """Assign "product_id" for saving form to DB and for coming back
        to product review page(redirection) after comment added(submit)
        """
        product_id = kwargs['pk']

        request.session.modified = True
        request.session['reviewed_products'].append(product_id)

        form = ReviewForm({'text': request.POST['text']})
        add_product_field = form.save(commit=False)
        if form.is_valid():
            add_product_field.product_id = product_id
            form.save()
            return redirect('product_detail', pk=product_id)
        else:
            return HttpResponse('Заполните форму корректно!')



