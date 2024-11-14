from django.db import models

from users.models import User


class Course(models.Model):
    """
    Модель курса
    title - название курса
    description - описание курса
    preview - превью курса (изображение)
    owner - автор курса
    """
    title = models.CharField(max_length=255, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание курса')
    preview = models.ImageField(upload_to='courses', verbose_name='Превью курса', null=True, blank='True')
    owner = models.ForeignKey(User, verbose_name='Aвтор курса', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='Курс урока', on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока')
    preview = models.ImageField(upload_to='courses', verbose_name='Превью урока', null=True, blank='True')
    video_url = models.CharField(max_length=255, verbose_name='Ссылка на видео урока', null=True, blank='True')
    owner = models.ForeignKey(User, verbose_name='Aвтор урока', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

class Subscribe(models.Model):
    """
    Модель подписки на курс
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribes')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscribes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Подписка: {self.user} - {self.course}"

    class Meta:
        unique_together = ['user', 'course']
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

class SubscribeMailing(models.Model):
    """
    Модель рассылки обновления курса
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс рассылки',
        related_name='mailings'
    )
    is_success = models.BooleanField(default=True, verbose_name='Статус рассылки')
    report = models.TextField(null=True, blank=True, verbose_name='Отчет в случае ошибки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания рассылки')

    def __str__(self):
        return f"Рассылка: {self.course} - {self.created_at}"

    class Meta:
        verbose_name = 'рассылка обновления курса'
        verbose_name_plural = 'рассылки обновления курса'
