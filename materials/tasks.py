import datetime

from celery import shared_task

from materials.models import Course
from materials.services import send_mail_update_course, block_inactive_users


@shared_task
def update_course(course_id: int, message: str = ''):
    """
    Отложенная задача:
    Рассылка уведомлений об обновлении курса
    :param course_id: id курса
    :param message: комментарий об обновлении
    :return:
    """
    course = Course.objects.filter(id=course_id).first()
    if course:
        send_mail_update_course(course, message)

@shared_task
def check_last_login():
    """
    Периодическая проверка активности пользователей
    """
    block_inactive_users()
