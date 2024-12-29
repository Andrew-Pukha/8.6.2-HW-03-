from django import template
import neapp.views as views
from neapp.models import *
from neapp.utils import menu

register = template.Library()


#61. Тэг, отображающий главное меню сайта на странице Авторизации.
@register.simple_tag
def get_menu():
    return menu


#-- Второй тип пользовательских тегов – включающий тег,
#-- позволяет дополнительно формировать свой собственный шаблон на основе
#-- некоторых данных и возвращать фрагмент HTML-страницы.


@register.inclusion_tag('neapp/list_categories.html')
def show_categories(cat_selected_id=0):
    cats = Category.objects.all()
    return {"cats": cats, "cat_selected": cat_selected_id}



#29. Функция, показывающая нам все тэги.
@register.inclusion_tag('neapp/list_tags.html')
def show_all_tags():
    return {"tags": TagPost.objects.all()}


