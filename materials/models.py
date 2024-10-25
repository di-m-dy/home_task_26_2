from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание курса')
    preview = models.ImageField(upload_to='courses', verbose_name='Превью курса', null=True, blank='True')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='Курс урока', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока')
    preview = models.ImageField(upload_to='courses', verbose_name='Превью урока', null=True, blank='True')
    video_url = models.CharField(max_length=255, verbose_name='Ссылка на видео урока', null=True, blank='True')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
