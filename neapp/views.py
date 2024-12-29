import uuid

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

#------------------------------------------------------------------------------filter
#from .filters import PosttFilter
#------------------------------------------------------------------------------filter

from .forms import *
from .models import *
from .utils import DataMixin



#13. Коллекция Главного меню (делаем кнопки ГМ кликабельными). Маршруты, функции представления и шаблоны уже прописаны:
menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}]





#Страница со списком ВСЕХ новостей (бывш. def news_page() или index()):
class NewsHome(DataMixin, ListView):
    template_name = 'neapp/news_page.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Post.published.all().select_related('cat')

# #------------------------------------------------------------------------------filter
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         self.filterset = PosttFilter(self.request.GET, queryset)
#         return self.filterset.qs
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['filterset'] = self.filterset
#         return context
# #------------------------------------------------------------------------------filter








#9. Страница О САЙТЕ новостей:
@login_required                     #63. Добавляем ограничение для неавторизованных пользователей
def about(request):
    contact_list = Post.published.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'neapp/about.html',
                  {'title': 'О сайте', 'menu': menu, 'page_obj': page_obj})








#Класс представления, показывающий страницу с подробным описанием и содержанием материала: (бывш. def show_post()):
class ShowPost(DataMixin, DetailView):
    template_name = 'neapp/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs),
                                      title='Главная страница',
                                      cat_selected=0,
                                      )

    #Метод, запрещающий вывод неопубликованного материала:
    def get_object(self, queryset=None):
        return get_object_or_404(Post.published, slug=self.kwargs[self.slug_url_kwarg])







#Класс представления, генерирующий страницу "Добавить статью": (бывш. def addpage()):
class AddPage(PermissionRequiredMixin, LoginRequiredMixin, View):      #63. Наследуемый класс LoginRequiredMixin накладывает ограничение на страницу Добавления Статей для неавторизированных пользователей.
    #накладываем ограничение прав для отдельных пользователей по добавлению материала с помощью класса PermissionRequiredMixin():
    permission_required = 'neapp.add_post'


    def get(self, request):
        form = AddPostForm()
        return render(request, 'neapp/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Post.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления поста')

        return render(request, 'neapp/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})

    #63. Проверяем: если данные пользователя верны и параметры добавления статьи тоже,
    #то Добавленному материалу (статье или новости) автоматически присваеиваем пользователя, добавившего материал (published_by).
    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)








#НОВЫЙ. Класс представления "редактировать статью":
class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'neapp/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    # накладываем ограничение прав для отдельных пользователей по редактированию материала с помощью класса PermissionRequiredMixin():
    permission_required = 'neapp.change_post'















#Класс представления, показывающий материал в той или иной категории (напр. новости - 4 материала, статьи - 3 материала): (бывш. def show_category()):
class NewsCategory(DataMixin, ListView):
    template_name = 'neapp/news_page.html'
    context_object_name = 'posts'
    allow_empty = False


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.id,
                                      )

    def get_queryset(self):
        return Post.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')









#5. Страница со списком КАТЕГОРИЙ новостей (выводится по запросу: #http://127.0.0.1:8000/cats/<int>/):
def categories(request, cat_id):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p >id:{cat_id}</p>")

#6. Страница со списком КАТЕГОРИЙ новостей (#http://127.0.0.1:8000/cats/<slug>/):
def categories_by_slug(request, cat_slug):
    print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p >slug:{ cat_slug }</p>")





#7. Страница АРХИВА новостей:
def archive(request, year):
    if year > 2025:
        return redirect('/')                                        #8. redirect - перенаправление с кодом 302.
    return HttpResponse(f"<h1>Архив по годам</h1><p >{year}</p>")























def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")





def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')






#Класс представления, сортирующий статьи по Тэгам: (бывш. def show_tag_postlist())****:
class TagPostList(DataMixin, ListView):
    template_name = 'neapp/news_page.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)


    def get_queryset(self):
        return Post.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')









