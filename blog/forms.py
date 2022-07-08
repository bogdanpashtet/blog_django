from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget

from .models import Tag, Profile


class ArticleForm(forms.Form):
    title = forms.CharField(required=True, max_length=200, label="Название:", widget=forms.TextInput(attrs={"class": "form-control"}))
    article_text = forms.CharField(label="Текст статьи:", required=False, widget=CKEditorWidget)
    # photo_preview = forms.ImageField(upload_to='photos_article/%Y/%M/%D', blank=True)
    is_published = forms.BooleanField(label="Опубликовано?:", initial=True, required=False)
    tags = forms.ModelMultipleChoiceField(required=True, queryset=Tag.objects.all(), label="Теги:", widget=forms.CheckboxSelectMultiple())


class RegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, max_length=200, label="Имя пользователя:", widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": None}))
    password1 = forms.CharField(required=True, max_length=200, label="Пароль:", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(required=True, max_length=200, label="Подтвердите пароль: :", widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class AuthForm(AuthenticationForm):
    username = forms.CharField(required=True, max_length=200, label="Имя пользователя:", widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": None}))
    password = forms.CharField(required=True, max_length=200, label="Пароль:", widget=forms.PasswordInput(attrs={"class": "form-control"}))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date', 'photo')


