from django.shortcuts import render, get_object_or_404, redirect
from .models import Articles, Tag
from django.contrib.auth.forms import UserCreationForm
from .forms import ArticleForm


def index(request):
    article_1 = Articles.objects.filter(is_published=True).prefetch_related('tags')
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
    articles = Articles.objects.filter(tags=tag_id, is_published=True).prefetch_related('tags')
    tag = Tag.objects.get(pk=tag_id)
    return render(request, 'blog/tag.html', {'title': tag, 'articles': articles, 'tag': tag})


def get_article(request, slug_name):
    articles = get_object_or_404(Articles, slug_name=slug_name)
    return render(request, 'blog/article.html', {'article': articles})


def add_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            article_text = form.cleaned_data["article_text"]
            is_published = form.cleaned_data["is_published"]
            tags = form.cleaned_data["tags"]
            article1 = Articles.objects.create(title=title, article_text=article_text, is_published=is_published)
            article1.tags.set(tags)
            article1.save()
            return redirect(article1)
    else:
        form = ArticleForm()
    return render(request, 'blog/add_article.html', {'title': "Добавить статью", 'form': form})
