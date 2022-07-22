from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from blog.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ------------------------ Main & Categories -------------------------------
    path('', Index.as_view(), name=''),
    path('tag/<int:tag_id>/', GetTag.as_view(), name='tag'),

    # --------------------------- Profile --------------------------------------
    path('profile/<int:pk>/', ViewProfile.as_view(), name='profile'),
    path('update_profile/<int:user_id>/', update_profile, name='update_profile'),

    # -------------------------- Articles --------------------------------------
    path('article/<slug:slug>/', ViewArticle.as_view(), name='article'),
    path('add_article/', AddArticle.as_view(), name='add_article'),
    path('edit_article/<slug:slug>/', UpdateArticle.as_view(), name='edit_article'),
    path('delete_article/<slug:slug>/', DeleteArticle.as_view(), name='delete_article'),

    # ---------------------------- User ----------------------------------------
    path('register/', ViewRegistration.as_view(), name='register'),
    path('login/', ViewLogin.as_view(), name='login'),
    path('logout/', ViewLogout.as_view(), name='logout'),
]

# ------------------------ Errors -------------------------------
handler404 = 'blog.views.page_not_found_view'
handler403 = 'blog.views.permission_denied_view'


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
