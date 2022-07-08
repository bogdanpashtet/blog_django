from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import Articles, Tag
from .forms import ArticleForm, RegistrationForm, AuthForm
from django.views.generic import UpdateView


def index(request):
    article_1 = Articles.objects.filter(is_published=True).prefetch_related('tags').order_by("-date_of_publishing")
    return render(request, 'blog/index.html', {'articles': article_1, 'title': "Главная"})


def profile(request):
    article_1 = Articles.objects.filter(owner=request.user).order_by("-date_of_publishing")
    return render(request, 'blog/profile.html', {'articles': article_1, 'title': "Профиль"})


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('profile')
        else:
            messages.error(request, 'Ошибка регистрации!')
    else:
        form = RegistrationForm()
    return render(request, 'blog/register.html', {'title': "Регистрация", 'form': form})


def authorization(request):
    if request.method == "POST":
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно авторизированны!')
            return redirect('profile')
        else:
            messages.error(request, 'Ошибка входа!')
    else:
        form = AuthForm()
    return render(request, 'blog/authorization.html', {'title': "Авторизация", 'form': form})


def user_logout(request):
    logout(request)
    return redirect('')


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
            owner = str(request.user)
            article1 = Articles.objects.create(title=title, article_text=article_text, is_published=is_published, owner=owner)
            article1.tags.set(tags)
            article1.save()
            return redirect(article1)
    else:
        form = ArticleForm()
    return render(request, 'blog/add_article.html', {'title': "Добавить статью", 'form': form})


def edit_article(request, slug_name):
    articles = get_object_or_404(Articles, slug_name=slug_name)
    title = articles.title
    article_text = articles.article_text
    is_published = articles.is_published
    tags = articles.tags.all()
    if request.method == "POST":
        articles.title = request.POST.get('title')
        articles.article_text = request.POST.get('article_text')
        articles.is_published = request.POST.get('is_published')
        if articles.is_published == "on":
            articles.is_published = True
        else:
            articles.is_published = False

        articles.tags.clear()
        for c in request.POST.get('tags'):
            print(c)
            articles.tags.add(c)
        articles.save()
        return redirect(articles)
    else:
        form = ArticleForm(initial={"title": title, "article_text": article_text, "is_published": is_published, "tags": tags})
        return render(request, "blog/edit_article.html", {'article': articles, 'form': form})


def delete_article(request, slug_name):
    article = Articles.objects.get(slug_name=slug_name)
    article.delete()
    return redirect('')

