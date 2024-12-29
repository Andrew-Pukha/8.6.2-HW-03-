from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


#66. Делаем авторизацию по e-mail:
class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None

    #66. Метод, отображающий Имя пользователя в Главном меню сайта, радом с кнопкой "Выйти":
    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None