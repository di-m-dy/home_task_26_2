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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribes')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscribes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Подписка: {self.user} - {self.course}"

    class Meta:
        unique_together = ['user', 'course']
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
