import datetime
import smtplib

import pytz
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER, TIME_ZONE
from materials.models import Course, SubscribeMailing
from users.models import User

PERIOD_DELTA_SUBSCRIBES = datetime.timedelta(days=4)
TIME_DELTA_LAST_LOGIN = datetime.timedelta(days=30)
ZONE = pytz.timezone(TIME_ZONE)

def send_mail_update_course(course: Course, message: str =''):
    current_date = datetime.datetime.now(ZONE)
    subscribe_mailing = SubscribeMailing.objects.filter(course=course).order_by('-created_at').first()
    if subscribe_mailing and subscribe_mailing.created_at + PERIOD_DELTA_SUBSCRIBES > current_date:
        return
    try:
        send = send_mail(
            subject=f"Обновление курса «{course}»",
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[i.user.email for i in course.subscribes.all()],
            fail_silently=False
        )
        SubscribeMailing.objects.create(
            course=course,
            is_success=bool(send)
        )
    except smtplib.SMTPException as e:
        SubscribeMailing.objects.create(
            course=course,
            is_success=False,
            report=e
        )

def block_inactive_users():
    """
    Проверка времени последнего входа пользователя
    Если пользователь не заходил более 30 дней, блокируем его
    """
    current_date = datetime.datetime.now(ZONE)
    users = User.objects.filter(is_active=True)
    for user in users:
        if user.last_login:
            if user.last_login + TIME_DELTA_LAST_LOGIN < current_date:
                user.is_active = False
                user.save()
        else:
            if user.date_joined + TIME_DELTA_LAST_LOGIN < current_date:
                user.is_active = False
                user.save()