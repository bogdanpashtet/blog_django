from django.shortcuts import render
from .models import Articles, Tag
from django.contrib.auth.forms import UserCreationForm


def index(request):
    article_1 = Articles.objects.all()
    return render(request, 'blog/index.html', {'articles': article_1, 'title': "Главная"})


def profile(request):
    return render(request, 'blog/profile.html', {'title': "Профиль"})


def article(request):
    return render(request, 'blog/article.html')


def about(request):
    return render(request, 'blog/about.html', {'title': "О нас"})


def register(request):
    form = UserCreationForm
    return render(request, 'blog/register.html', {'title': "Регистрация", 'form': form})


def login(request):
    return render(request, 'blog/register.html', {'title': "Авторизоваться"})


def get_tag(request, tag_id):
    articles = Articles.objects.filter(genre=tag_id)
    tag = Tag.objects.get(pk=tag_id)
    return render(request, 'blog/tag.html', {'title': tag, 'articles': articles, 'tag': tag})