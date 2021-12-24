from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        max_length=150,
        unique=True,
        verbose_name='Почта',
    )
    username = models.CharField(
        max_length=150,
        blank=False,
        unique=True,
        verbose_name='Имя пользователя',
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Фамилия',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return self.email


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь-подписчик',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Пользователь (на кого подписаны)',
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'following'],
                       name='unique_following')]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
