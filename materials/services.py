import datetime
import smtplib

import pytz
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER, TIME_ZONE
from materials.models import Course, SubscribeMailing

PERIOD_DELTA = datetime.timedelta(days=4)
ZONE = pytz.timezone(TIME_ZONE)

def send_mail_update_course(course: Course, message: str =''):
    current_date = datetime.datetime.now(ZONE)
    subscribe_mailing = SubscribeMailing.objects.filter(course=course).order_by('-created_at').first()
    print(f"Last mailing: {subscribe_mailing.created_at if subscribe_mailing else None}")
    print(f"Current date: {current_date}")
    if subscribe_mailing and subscribe_mailing.created_at + PERIOD_DELTA > current_date:
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