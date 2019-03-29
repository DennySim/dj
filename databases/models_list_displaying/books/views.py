from django.views import generic
# from books.models import Book

from .models import Book


class BookListView(generic.ListView):
    template_name = 'books/book_list.html'
    model = Book

    def get_context_data(self, **kwargs):
        context = {}
        date = self.kwargs

        if date:
            queryset = Book.objects.filter(pub_date=date['date'])

            queryset_next_date = Book.objects \
                .filter(pub_date__gt=date['date']).order_by('pub_date')[:1]
            if queryset_next_date:

                context['next_page_url'] = str(Book.objects \
                    .filter(name=queryset_next_date[0].name)[0].pub_date)

            queryset_prev_date = Book.objects \
                .filter(pub_date__lt=date['date']).order_by('-pub_date')[:1]
            if queryset_prev_date:

                context['prev_page_url'] = str(Book.objects
                    .filter(name=queryset_prev_date[0].name)[0].pub_date)

            context['book'] = queryset

        else:
            queryset = Book.objects.all()
            context['book'] = queryset

        return context
