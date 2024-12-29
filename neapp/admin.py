from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import *



#40. Добавим свой собственный фильтр.
#--Например, давайте будем отбирать отредактированный материал и неотредактированный.
class EditorFilter(admin.SimpleListFilter):
    title = 'Редактор материала'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('editor', 'Редакция пройдена'),
            ('no_editor', 'Редакция не пройдена'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'editor':
            return queryset.filter(editor__isnull=False)
        elif self.value() == 'no_editor':
            return queryset.filter(editor__isnull=True)






@admin.register(Post)
#38. Класс для модели Post(посты/материалы):
class NeappAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'cat', 'photo', 'post_photo', 'tags', 'author']
    readonly_fields = ['post_photo']
    prepopulated_fields = {"slug": ("title",)}                                          #41. Слаг формируется автоматически.
    list_display = ('id', 'title', 'post_photo', 'created_at', 'is_published', 'cat')
    list_display_links = ('id', 'title')
    ordering = ['created_at', 'title']
    list_editable = ('is_published', 'cat')
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = [EditorFilter, 'cat__name', 'is_published']
    save_on_top = True


    #50. Метод (декоратор) отображающий мини-фото в админ-панели:
    @admin.display(description="Изображение")
    def post_photo(self, neapp: Post):
        if neapp.photo:
            return mark_safe(f"<img src='{neapp.photo.url}' width=50>")
        return "Без фото"



    #39. Добавим еще одно действие, которое будет устанавливать статус «Опубликовано» всем выделенным статьям:
    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Post.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

    #39. Добавим еще одно действие, которое будет устанавливать статус «Снять с публикации» всем выделенным статьям:
    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Post.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!", messages.WARNING)



#38. Класс для модели Category(категории):
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')




#admin.site.register(Post, NeappAdmin, CategoryAdmin)

