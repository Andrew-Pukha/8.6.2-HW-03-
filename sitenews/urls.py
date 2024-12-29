"""
URL configuration for sitenews project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from neapp import views
from neapp.views import page_not_found
from sitenews import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('neapp.urls')),                #http://127.0.0.1:8000 - Страница приложения neapp со списком материала.
    path('users/', include('users.urls', namespace='users')),    #59
    path('cats/', views.categories),                #http://127.0.0.1:8000/cats/
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Новости и статьи"
handler404 = page_not_found

