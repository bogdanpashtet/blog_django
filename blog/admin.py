from django.contrib import admin

from .models import Users, Articles


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'is_active', 'role')


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'is_published')
