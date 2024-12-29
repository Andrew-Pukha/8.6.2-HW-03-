from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.template.defaultfilters import slugify
from django.urls import reverse




#41. Данный костыль необходим, чтобы формируемый автоматически на основе заголовка slug вновь создаваемой записи мог быть интерпретирован латиницей на русский язык:
def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))



class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Post.Status.PUBLISHED)




class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # 1. суммарный рейтинг каждой статьи автора умножается на 3
        post_rating = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum'] or 0
        post_rating *= 3

        # 2. суммарный рейтинг всех комментариев автора
        comment_rating = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum'] or 0

        # 3. суммарный рейтинг всех комментариев к статьям автора
        post_comments_rating = Comment.objects.filter(post__author=self).aggregate(Sum('rating'))['rating__sum'] or 0

        # Итоговый рейтинг
        self.rating = post_rating + comment_rating + post_comments_rating
        self.save()





class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})




class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=POST_TYPES, default=ARTICLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    #categories = models.ManyToManyField(Category, through='PostCategory')       #--
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(blank=True, verbose_name="Текст материала")
    rating = models.IntegerField(default=0)
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name="Статус")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    cat = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name="Тэг")   #-- связь Многие ко многим(добавление тэгов)
    editor = models.OneToOneField('Editor', on_delete=models.SET_NULL, null=True, blank=True, related_name='material', verbose_name="Редактор материала")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Фото")
    published_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True,
                               default=None)

    objects = models.Manager()
    published = PublishedModel()

    #-- Материал выводится в порядке от более свежей к самой старой:
    class Meta:
        verbose_name = 'Авторские материалы'
        verbose_name_plural = 'Авторские материалы'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + '...' if len(self.content) > 124 else self.content

    #41. Функция save() формирует в точности такой же slug, как и название заголовка:
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit_to_eng(self.title))
    #     super().save(*args, **kwargs)







class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)





class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()  # Текст комментария
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания
    rating = models.IntegerField(default=0)  # Рейтинг комментария

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.tag




#30. Модель (таблица) "Редактор", который отредактировал материал:
class Editor(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)

    def __str__(self):
        return self.name





#49. Таблица, хранящая ссылки на загруженные файлы:
class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')