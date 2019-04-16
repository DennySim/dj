from django.shortcuts import render, redirect
from .models import Article, Profile, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


def logging_in(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(request,
                                username=request.POST['username'],
                                password=request.POST['password'])
            if user is not None:
                login(request, user)
                return redirect('articles_list')
    if request.method == 'GET':
        print('=====')
        login_form = AuthenticationForm()
        context = {'login_form': login_form}
        return render(
            request,
            'articles.html', context
        )


def show_articles(request):

    context = {}
    articles = Article.objects.filter(paid=False)

    # Активируется при нажатии кнопки "Подписаться"
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        profile = Profile.objects.get(user_id=user.pk)
        profile.paid_subscription = True
        profile.save()

    if request.user.is_authenticated:

        user = User.objects.get(username=request.user.username)
        if user.profile.paid_subscription:
            articles = Article.objects.all()
        else:
            context['subscribe'] = True
    else:

        login_form = AuthenticationForm()
        context['login_form'] = login_form

    context['articles'] = articles

    return render(
        request,
        'articles.html', context
        )


def show_article(request, **kwargs):

    context = {'article': Article.objects.get(id=kwargs['id'])}
    return render(
        request,
        'article.html', context
    )
