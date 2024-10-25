from django.contrib.auth.models import AbstractUser
from django.db import models
from phone_field import PhoneField

from materials.models import Course, Lesson


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


class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ('card', 'Кредитная карта'),
        ('cash', 'Оплата наличными')
    ]

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course,
        verbose_name='Оплаченный курс',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    lesson = models.ForeignKey(
        Lesson,
        verbose_name='Оплаченный урок',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    method = models.CharField(max_length=4, verbose_name='Метод оплаты', choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"{self.user}: {self.course or self.lesson} = {self.cost} руб."

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплата'
