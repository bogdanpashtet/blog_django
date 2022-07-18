from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Articles, Tag, Profile
from .forms import ArticleForm, RegistrationForm, AuthForm, UserForm, ProfileForm
from django.core.exceptions import PermissionDenied


def index(request):
    article_1 = Articles.objects.filter(is_published=True).prefetch_related('tags').order_by("-date_of_publishing")
    return render(request, 'blog/index.html', {'articles': article_1, 'title': "Главная"})


def profile(request, user_id):
    name1 = get_object_or_404(User, id=user_id)
    profile1 = get_object_or_404(Profile, user=name1)
    if request.user == name1:
        article_1 = Articles.objects.filter(owner=name1).order_by("-date_of_publishing")
    else:
        article_1 = Articles.objects.filter(owner=name1, is_published=True).order_by("-date_of_publishing")
    return render(request, 'blog/profile.html', {
        'user_form': name1,
        'profile_form': profile1,
        'articles': article_1,
        'title': "Профиль"
    })


def register(request):
    if request.user.id is None:
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Вы успешно зарегистрированы!')
                return redirect('profile', user_id=request.user.id)
            else:
                messages.error(request, 'Ошибка регистрации!')
        else:
            form = RegistrationForm()
        return render(request, 'blog/register.html', {'title': "Регистрация", 'form': form})
    else:
        return redirect('profile', user_id=request.user.id)


def authorization(request):
    if request.user.id is None:
        if request.method == "POST":
            form = AuthForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                messages.success(request, 'Вы успешно авторизированны!')
                return redirect('profile', user_id=request.user.id)
            else:
                messages.error(request, 'Ошибка входа!')
        else:
            form = AuthForm()
        return render(request, 'blog/authorization.html', {'title': "Авторизация", 'form': form})
    else:
        return redirect('profile', user_id=request.user.id)


def user_logout(request):
    logout(request)
    return redirect('')


def get_tag(request, tag_id):
    articles = Articles.objects.filter(tags=tag_id, is_published=True).prefetch_related('tags')
    tag = Tag.objects.get(pk=tag_id)
    return render(request, 'blog/index.html', {'title': tag, 'articles': articles, 'tag': tag})


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
            owner = str(request.user.id)
            article1 = Articles.objects.create(title=title, article_text=article_text, is_published=is_published, owner_id=owner)
            article1.tags.set(tags)
            article1.save()
            return redirect(article1)
    else:
        form = ArticleForm()
    return render(request, 'blog/add_article.html', {'title': "Добавить статью", 'form': form})


def edit_article(request, slug_name):
    articles = get_object_or_404(Articles, slug_name=slug_name)
    if request.user.id == articles.owner_id:
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
            for c in request.POST.getlist('tags'):
                print(c)
                articles.tags.add(c)
            articles.save()
            return redirect(articles)
        else:
            form = ArticleForm(initial={"title": title, "article_text": article_text, "is_published": is_published, "tags": tags})
            return render(request, "blog/edit_article.html", {'title': "Изменить статью", 'article': articles, 'form': form})
    else:
        raise PermissionDenied


def delete_article(request, slug_name):
    article = Articles.objects.get(slug_name=slug_name)
    if request.user.id == article.owner_id:
        article.delete()
        return redirect('profile', user_id=request.user.id)
    else:
        raise PermissionDenied


@login_required
@transaction.atomic
def update_profile(request, user_id):
    name1 = get_object_or_404(User, id=user_id)
    if request.user == name1:
        profile1 = get_object_or_404(Profile, user_id=user_id)
        article_1 = Articles.objects.filter(owner=name1).order_by("-date_of_publishing")
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=name1)
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile1)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Ваш профиль был успешно обновлен!')
                return redirect('profile', user_id=request.user.id)
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки.')
        else:
            user_form = UserForm(instance=name1)
            profile_form = ProfileForm(instance=profile1)
        return render(request, 'blog/update_profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'articles': article_1,
            'title': "Профиль"
        })
    else:
        raise PermissionDenied


def page_not_found_view(request, exception):
    return render(request, 'blog/base_errors.html', {
        'title': "Ошибка 404",
        'error_number': 404,
        'error_text': "Страница не найдена.",
        'error_description': "Страница, которую Вы ищите, не существует."
    }, status=404)


def permission_denied_view(request, exception):
    return render(request, 'blog/base_errors.html', {
        'title': "Ошибка 403",
        'error_number': 403,
        'error_text': "Доступ к данной странице запрещен.",
        'error_description': "У Вас недостаточно прав пользователя, чтобы перейти на данную страницу."
    }, status=403)
