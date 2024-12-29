from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import *


#46. Создаём свой собственный валидатор, который будет определять допустимые символы и выдавать ошибку,
#-- если символы не те, что указаны:
@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code, params={"value": value})






#44. Создаём первую форму, которая будет описывать добавление новых статей с сайта (а не с админ-панели):
class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категория")
    author = forms.ModelChoiceField(queryset=Author.objects.all(), empty_label="Автор не выбран", label="Автор")

    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'photo', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }
        labels = {'slug': 'URL'}


    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')

        return title








#48. Данный класс позволяет загружать именно графические файлы.
class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Изображение")





