from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from blog.views import index, profile, article, register, get_tag, get_article, add_article, authorization, user_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name=''),
    path('profile/', profile, name='profile'),
    path('article/', article, name='article'),
    path('add_article/', add_article, name='add_article'),
    path('register/', register, name='register'),
    path('authorization/', authorization, name='authorization'),
    path('logout/', user_logout, name='logout'),
    path('tag/<int:tag_id>/', get_tag, name='tag'),
    path('article/<slug:slug_name>/', get_article, name='article')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
