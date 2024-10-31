from rest_framework.serializers import ModelSerializer

from users.models import User
from payments.serializers import PaymentSerializer


class UserSerializer(ModelSerializer):
    payments = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'

class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'date_joined', 'first_name', 'city')


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
