from django.db import models
from users.models import User
from materials.models import Course, Lesson

class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ('card', 'Кредитная карта'),
        ('cash', 'Оплата наличными')
    ]

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='payments')
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
    created_at = models.DateTimeField(verbose_name='Дата оплаты')

    def __str__(self):
        return f"{self.user}: {self.course or self.lesson} = {self.cost} руб."

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплата'
