from django.contrib import admin

from .models import Profile, Articles, Tag


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_genre', 'owner', 'date_of_publishing', 'is_published')


@admin.register(Tag)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
