from django.shortcuts import render, redirect
from .models import Article, Profile, User
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm


def logging_in(request):

    if request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('articles_list')

    if request.method == 'GET':
        login_form = AuthenticationForm()
        context = {'login_form': login_form}
        return render(
                    request,
                    'articles.html', context
                )


def show_articles(request):

    context = {}
    articles = Article.objects.all()

    if 'id' in request.GET:
        context = {'article': articles.get(id=request.GET.get('id'))}
        return render(
            request,
            'article.html', context
        )

    if not request.user.is_authenticated:

        articles = articles.filter(paid=False)
        login_form = AuthenticationForm()
        context['login_form'] = login_form

    else:
        print('auth')
        user = User.objects.get(username=request.user)
        if hasattr(user, 'profile'):
            if not user.profile.paid_subscription:
                context['subscribe'] = True
                articles = articles.filter(paid=False)
        else:
            context['subscribe'] = True
            articles = articles.filter(paid=False)

    context['articles'] = articles

    return render(
        request,
        'articles.html', context
        )


def subscribe(request):

    if request.method == 'POST':

        user = User.objects.get(username=request.user)
        profile = Profile(user=user,
                          paid_subscription=True
                          )
        profile.save()
        return redirect('articles_list')

    if request.method == 'GET':
        return render(
            request,
            'subscribe-form.html'
        )


