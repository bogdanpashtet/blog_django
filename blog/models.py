from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    nickname = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='photos/%Y/%M/%D')
    email = models.EmailField(unique=True, default="aaa@aa.com")
    date_of_creation = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    role = models.IntegerField(default=0)


class Articles(models.Model):
    title = models.CharField(max_length=200, default="Enter the name please")
    owner = models.CharField(max_length=50)
    article_text = models.TextField(blank=True)
    date_of_publishing = models.DateTimeField(auto_now_add=True)
    # photo_preview = models.ImageField(upload_to='photos_article/%Y/%M/%D')
    slug_name = models.SlugField(unique=True, max_length=200, default=0)
