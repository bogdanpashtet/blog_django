from django.contrib import admin

from .models import Profile, Articles


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'is_published')
