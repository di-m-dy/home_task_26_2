import json

from django.core.management import BaseCommand

from config.settings import BASE_DIR
from users.models import Payment, User
from materials.models import Course, Lesson
from users.serializers import PaymentSerializer



class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(BASE_DIR / 'default_data/payment_data.json') as file:
            data = json.load(file)
        payments = data['payments']

        for i in payments:
            serialize = PaymentSerializer(data=i)
            if serialize.is_valid():
                serialize.save()
            else:
                print(f"Payment #{i['id']} not saved")
