from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Articles, Tag, Profile
from .forms import ArticleForm, RegistrationForm, AuthForm, UserForm, ProfileForm
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView


# ----------- Main & Categories ----------------
class Index(ListView):
    model = Articles
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    extra_context = {'title': 'Главная'}

    def get_queryset(self):
        return Articles.objects.filter(is_published=True).prefetch_related('tags').order_by("-date_of_publishing")


class GetTag(ListView):
    model = Articles
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(pk=self.kwargs['tag_id'])
        context['tag'] = context['title']
        return context

    def get_queryset(self):
        return Articles.objects.filter(tags=self.kwargs['tag_id'], is_published=True).prefetch_related('tags').order_by(
            '-date_of_publishing')


# --------------- Profile ----------------------
class ViewProfile(DetailView):
    model = User, Profile
    template_name = 'blog/profile.html'
    allow_empty = False
    context_object_name = 'user_form'
    extra_context = {'title': "Профиль"}

    def get_queryset(self):
        return User.objects.filter(pk=self.kwargs['pk']).prefetch_related('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.id == self.kwargs['pk']:
            context['articles'] = Articles.objects.filter(owner_id=self.kwargs['pk']).order_by("-date_of_publishing")
        else:
            context['articles'] = Articles.objects.filter(owner_id=self.kwargs['pk'], is_published=True).order_by(
                "-date_of_publishing")
        return context


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


# --------------- Articles ----------------
class ViewArticle(DetailView):
    model = Articles
    context_object_name = 'article'
    template_name = 'article/article.html'
    slug_url_kwarg = 'slug'


class AddArticle(CreateView):
    form_class = ArticleForm
    extra_context = {'title': "Добавить статью"}
    template_name = 'article/add_article.html'

    def form_valid(self, form):
        article1 = Articles.objects.create(
            title=form.cleaned_data["title"],
            article_text=form.cleaned_data["article_text"],
            is_published=form.cleaned_data["is_published"],
            owner_id=self.request.user.id
        )
        tags = form.cleaned_data["tags"]
        article1.tags.set(tags)
        article1.save()
        return redirect(article1)


def edit_article(request, slug):
    articles = get_object_or_404(Articles, slug=slug)
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
            form = ArticleForm(
                initial={"title": title, "article_text": article_text, "is_published": is_published, "tags": tags})
            return render(request, "article/edit_article.html",
                          {'title': "Изменить статью", 'article': articles, 'form': form})
    else:
        raise PermissionDenied


def delete_article(request, slug):
    article = Articles.objects.get(slug=slug)
    if request.user.id == article.owner_id:
        article.delete()
        return redirect('profile', user_id=request.user.id)
    else:
        raise PermissionDenied


# --------------- User ----------------
class ViewRegistration(CreateView, SuccessMessageMixin):
    form_class = RegistrationForm
    extra_context = {'title': "Регистрация"}
    template_name = 'registration/register.html'
    success_message = "Ваш профиль был успешно создан! Войдите на свою новую страницу."
    success_url = reverse_lazy('login')


class ViewLogin(LoginView, SuccessMessageMixin):
    authentication_form = AuthForm
    extra_context = {'title': "Авторизация"}
    redirect_authenticated_user = True
    success_message = 'Вы успешно авторизированны!'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка входа!')
        return super().form_invalid(form)


class ViewLogout(LogoutView):
    next_page = ''

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы успешно вышли со своей страницы!')
        return super().dispatch(request, *args, **kwargs)


# --------------- Errors ----------------
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
