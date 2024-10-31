from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from payments.models import Payment

from payments.serializers import PaymentSerializer



class PaymentsListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ('course', 'lesson')
    ordering_fields = ('created_at',)
    search_fields = ('method',)
