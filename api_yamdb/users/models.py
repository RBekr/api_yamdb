from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

ROLE_CHOICES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ'),
]


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        max_length=254,
    )
    username = models.CharField(
        unique=True,
        max_length=150,
        validators=[UnicodeUsernameValidator()]
    )
    password = models.CharField(max_length=20, null=True)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )
    date_joined = models.DateTimeField(null=True)
    bio = models.TextField(
        blank=True,
        null=True
    )
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs) -> None:
        if self.is_superuser:
            self.role = 'admin'
        return super(User, self).save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
