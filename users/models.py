from django.contrib.auth.models import AbstractUser
from django.db import models
from phone_field import PhoneField


class User(AbstractUser):
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(unique=True, verbose_name='Email пользователя')
    phone = PhoneField(verbose_name='Телефон пользователя', null=True, blank=True)
    city = models.CharField(max_length=100, verbose_name='Город пользователя', null=True, blank=True)
    avatar = models.ImageField(upload_to='users/avatars', verbose_name='Изображение профиля', null=True, blank=True)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
