from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse




class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Контент')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Изображение')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Изменено')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    owner_name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор',
                                   related_name='my_news')
    readers = models.ManyToManyField(User, through='UserNewsRelation', related_name='news')

    author_name = models.CharField(max_length=255, verbose_name='Создатель')

    rating = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True)

    # comments = GenericRelation('comments')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-time_created']


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class UserNewsRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Shit'),
        (2, 'Not bad'),
        (3, 'Fine'),
        (4, 'OK'),
        (5, 'Amazing'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    like = models.BooleanField(default=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f'{self.user.username}: Book: {self.news}, RATE: {self.rate}'

    def save(self, *args, **kwargs):
        from news.logic import set_rating

        creating = not self.pk
        old_rating = self.rate

        super().save(*args, **kwargs)

        new_rating = self.rate
        if old_rating != new_rating or creating:
            set_rating(self.news)

# class Comments(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор', on_delete=models.CASCADE)
#     text = models.TextField(verbose_name='Текст комментария')
#     parent = models.ForeignKey(
#         'self',
#         verbose_name='Родительский комментарий',
#         blank=True,
#         null=True,
#         related_name='comment_children',
#         on_delete=models.CASCADE
#     )
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     timestamp = models.DateTimeField(auto_now=True, verbose_name='Дата создания комментария')
#     is_child = models.BooleanField(default=False)
#
#     def __str__(self):
#         return str(self.id)
#
#     @property
#     def get_parent(self):
#         if not self.parent:
#             return ''
#         return self.parent
