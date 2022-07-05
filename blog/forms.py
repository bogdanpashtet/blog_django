from django import forms
from .models import Tag

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email')
#
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('url', 'location', 'company')


class ArticleForm(forms.Form):
    title = forms.CharField(required=True, max_length=200, label="Название:", widget=forms.TextInput(attrs={"class": "form-control"}))
    # owner = models.CharField(max_length=200, default="Enter the owner of this article", verbose_name="Владелец")
    article_text = forms.CharField(label="Текст статьи:", required=False, widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}))
    # photo_preview = forms.ImageField(upload_to='photos_article/%Y/%M/%D', blank=True)
    is_published = forms.BooleanField(label="Опубликовано?:", initial=True)
    genre = forms.ModelMultipleChoiceField(required=True, queryset=Tag.objects.all(), label="Теги:", widget=forms.SelectMultiple(attrs={"class": "form-control"}))
