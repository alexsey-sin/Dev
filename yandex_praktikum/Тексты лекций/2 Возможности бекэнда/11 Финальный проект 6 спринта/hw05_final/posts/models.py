from django.db import models
from django.contrib.auth import get_user_model
from .validators import validate_not_empty

User = get_user_model()


class Group(models.Model):
    objects = None
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=200,
        help_text='Дайте короткое название группе',
    )
    slug = models.SlugField(
        verbose_name='Адрес',
        unique=True,
        help_text='Укажите адрес для страницы группы',
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Укажите краткое описание группы',
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    objects = None
    text = models.TextField(
        verbose_name='Текст',
        help_text='Начните писать здесь',
        validators=[validate_not_empty]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='author_posts',
    )
    group = models.ForeignKey(
        Group,
        verbose_name='Группа',
        on_delete=models.SET_NULL,
        related_name='group_posts',
        blank=True, null=True,
    )
    image = models.ImageField(
        verbose_name='Изображение',
        help_text='Загрузите изображение',
        upload_to='posts/',
        blank=True, null=True,
    )

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        verbose_name='Пост',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Начните писать здесь комментарий',
        validators=[validate_not_empty]
    )
    created = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='following',
    )
