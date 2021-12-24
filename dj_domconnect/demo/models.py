# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


# class UserRole(models.TextChoices):
    # USER = 'user'
    # MODERATOR = 'moderator'
    # ADMIN = 'admin'


# class User(AbstractUser):
    # email = models.EmailField('Email', unique=True, blank=False)
    # role = models.CharField('Роль', max_length=20, choices=UserRole.choices,
                            # default=UserRole.USER)
    # bio = models.TextField('О себе', max_length=200, blank=True)

    # class Meta:
        # ordering = ['id']

    # @property
    # def is_moderator(self):
        # return self.role == UserRole.MODERATOR

    # @property
    # def is_admin(self):
        # return self.role == UserRole.ADMIN or self.is_staff



