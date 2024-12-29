from django.contrib import admin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from django.urls import path, reverse_lazy
from users import views



#PasswordChangeView – для обработки формы изменения пароля;
#PasswordChangeDoneView – для отображения результата успешного изменения пароля.

app_name = "users"

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),           #59. Маршрут для отображения и обработки формы авторизации пользователя.
    path('logout/', views.logout_user, name='logout'),                 #59. Маршрут для выхода пользователя.

    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"), name="password_change_done"),

    path('register/', views.RegisterUser.as_view(), name='register'),  #64. Маршрут для регистрации новых пользователей.
    path('profile/', views.ProfileUser.as_view(), name='profile'),     #66. Маршрут для перенаправления пользователя, после редактирования и сохранения своего профиля.

    #Ссылки на восстановление и сброса инструкций на почту:
    path('password-reset/',
         PasswordResetView.as_view(
             template_name="users/password_reset_form.html",
             email_template_name="users/password_reset_email.html",
             success_url=reverse_lazy("users:password_reset_done")
         ), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name = "users/password_reset_done.html"), name='password_reset_done'),

    #Ссылки формирование одноразовой ссылки:
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name="users/password_reset_confirm.html",
             success_url=reverse_lazy("users:password_reset_complete")
         ), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name='password_reset_complete'),

]