from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Пользователь"
        self.fields['password'].label = "Пароль"


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Пользователь"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Подтверждение пароля"


def home(request):
    return render(
        request,
        'home.html'
    )


def signup(request):

    if request.method == 'POST':
        reg_form = CustomUserCreationForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save()
            login(request, user)
        return redirect('auth_home')
    else:
        reg_form = CustomUserCreationForm()
    return render(
        request,
        'signup.html', {'form': reg_form}
    )


def logging_in(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('auth_home')
    else:
        login_form = CustomAuthenticationForm()
    return render(request, 'signup.html', {'login_form': login_form})


def logging_out(request):

    logout(request)
    logout_message = "Спасибо, что посетили наш сайт, приходите еще!"
    return render(request, 'home.html', {'text': logout_message})
