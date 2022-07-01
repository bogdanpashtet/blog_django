from django.shortcuts import render
from django.http import HttpResponse
from .models import Articles


def index(request):
    article = Articles.objects.all()
    return render(request, 'blog/index.html', {'articles': article, 'title': "Главная"})


def profile(request):
    return render(request, 'blog/profile.html')


def article(request):
    return render(request, 'blog/article.html')
