from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    email = models.EmailField('Email', unique=True, blank=False)
    role = models.CharField('Роль', max_length=20, choices=UserRole.choices,
                            default=UserRole.USER)
    bio = models.TextField('О себе', max_length=200, blank=True)

    class Meta:
        ordering = ['id']

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_staff


class Category(models.Model):
    name = models.CharField('Название', max_length=150)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название', max_length=150)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=300)
    year = models.PositiveSmallIntegerField('Год создания')
    description = models.TextField('Описание', null=True)
    category = models.ForeignKey(
        Category, verbose_name='Категория',
        on_delete=models.SET_NULL, null=True, related_name='titles',
    )
    genre = models.ManyToManyField(Genre, verbose_name='Жанры')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.text
