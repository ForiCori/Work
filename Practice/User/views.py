from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView


class UserLogin(LoginView):
    form_class = AuthenticationForm
    template_name = 'user/login.html'
    extra_context = {'title': 'Вход',
                     'button': 'Вход'}

    def get_success_url(self):
        return reverse_lazy('main')


class UserRegistration(CreateView):
    form_class = UserCreationForm
    template_name = 'user/login.html'
    extra_context = {'title': 'Регистрация',
                     'button': 'Зарегистрироваться'}

    def get_success_url(self):
        return reverse_lazy('login')


def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('main'))
