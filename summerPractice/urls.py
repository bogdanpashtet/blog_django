from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from blog.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name=''),
    path('tag/<int:tag_id>/', GetTag.as_view(), name='tag'),

    path('profile/<int:user_id>/', profile, name='profile'),
    path('update_profile/<int:user_id>/', update_profile, name='update_profile'),

    # path('article/<slug:slug_name>/', get_article, name='article'),
    path('article/<slug:slug>/', ViewArticle.as_view(), name='article'),
    path('add_article/', add_article, name='add_article'),
    path('edit_article/<slug:slug>/', edit_article, name='edit_article'),
    path('delete_article/<slug:slug>/', delete_article, name='delete_article'),

    path('register/', register, name='register'),
    path('authorization/', authorization, name='authorization'),
    path('logout/', user_logout, name='logout'),
]


handler404 = 'blog.views.page_not_found_view'

handler403 = 'blog.views.permission_denied_view'


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




