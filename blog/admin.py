from django.contrib import admin

from .models import Articles, Tag


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_genre', 'owner', 'date_of_publishing', 'is_published')
    prepopulated_fields = {"slug": ('title', )}


@admin.register(Tag)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
