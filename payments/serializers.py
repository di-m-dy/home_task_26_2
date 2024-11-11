from django.core.serializers import serialize
from rest_framework.serializers import ModelSerializer

from payments.models import Payment


class PaymentSerializer(ModelSerializer):
    """
    Сериализатор для платежей
    """
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentCreateSerializer(ModelSerializer):
    """
    Сериализатор для платежей
    """
    class Meta:
        model = Payment
        fields = ('cost', 'course', 'lesson', 'method', 'payment_link', 'created_at')

