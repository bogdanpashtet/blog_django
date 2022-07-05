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
    title = forms.CharField(max_length=200)
    # owner = models.CharField(max_length=200, default="Enter the owner of this article", verbose_name="Владелец")
    article_text = forms.CharField()
    # photo_preview = forms.ImageField(upload_to='photos_article/%Y/%M/%D', blank=True)
    slug_name = forms.SlugField()
    is_published = forms.BooleanField()
    genre = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
