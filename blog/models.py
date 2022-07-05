from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.template.defaultfilters import slugify as django_slugify

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def slugify(s):
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/%Y/%M/%D', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('tag', kwargs={"tag_id": self.pk})

    def __str__(self):
        return self.name


class Articles(models.Model):
    title = models.CharField(max_length=200, default="Enter the name please", verbose_name="Заголовок")
    # owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Владелец")
    owner = models.CharField(max_length=200, default="admin", verbose_name="Владелец")
    article_text = models.TextField(blank=True, verbose_name="Текст статьи")
    date_of_publishing = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    photo_preview = models.ImageField(upload_to='photos_article/%Y/%M/%D', blank=True)
    slug_name = models.SlugField(max_length=200, db_index=True)
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано?")
    genre = models.ManyToManyField(Tag, help_text="Выберете тематику статьи", verbose_name="Теги")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def get_genre(self):
        return " ".join([str(p) for p in self.genre.all()])

    def get_absolute_url(self):
        return reverse('article', kwargs={'slug_name': self.slug_name})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug_name = slugify(self.title)
        super(Articles, self).save(*args, **kwargs)
