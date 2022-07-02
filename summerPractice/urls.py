from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from blog.views import index, profile, article

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('profile/', profile, name='profile'),
    path('article/', article, name='article')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
