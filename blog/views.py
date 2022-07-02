from django.shortcuts import render
from .models import Articles


def index(request):
    article_1 = Articles.objects.all()
    return render(request, 'blog/index.html', {'articles': article_1, 'title': "Главная"})


def profile(request):
    return render(request, 'blog/profile.html')


def article(request):
    return render(request, 'blog/article.html')
