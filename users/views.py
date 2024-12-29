from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


#62. Класс представления для отображения и обработки формы авторизации пользователя:
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}



#59. Функция представления для выхода пользователя:
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))     #после выхода из системы, пользователь вновь перенаправлятся на страницу авторизации.





#65. Объявим класс представления для регистации новых пользователей:
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')





#66. Класс представления ProfileUser() отображает форму профиля пользователя:
class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    #Метод get_success_url() нужен для того, чтобы Django знал, куда перенаправлять, когда мы меняем и сохраняем поля профиля пользователя,
    #a перенаправляться мы будем на текущую страницу:
    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user





#67. Класс представления для изменения пароля пользователя в его профиле:
class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}






# В классе-представлении редактирования профиля добавить проверку аутентификации.




# Реализовать возможность регистрации через Yandex-аккаунт.
# Создать группы common и authors.
# Реализовать автоматическое добавление новых пользователей в группу common.
# Создать возможность стать автором (быть добавленным в группу authors).
# Для группы authors предоставить права создания и редактирования объектов модели Post (новостей и статей).
# В классах-представлениях добавления и редактирования новостей и статей добавить проверку прав доступа.
# Исходный код залить в git-репозиторий.