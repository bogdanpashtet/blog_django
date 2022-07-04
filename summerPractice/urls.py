from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from blog.views import index, profile, article, about, register, login, get_tag

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name=''),
    path('profile/', profile, name='profile'),
    path('article/', article, name='article'),
    path('about/', about, name='about'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('tag/<int:tag_id>', get_tag)
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
