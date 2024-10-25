from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class PaymentsListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ('course', 'lesson')
    ordering_fields = ('created_at',)
    search_fields = ('method',)
