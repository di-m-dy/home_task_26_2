from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from django_filters import rest_framework as filters
from payments.models import Payment

from payments.serializers import PaymentSerializer, PaymentCreateSerializer
from payments.services import create_product, create_price, create_checkout_session


class PaymentsListAPIView(ListAPIView):
    """
    Список платежей
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ('course', 'lesson')
    ordering_fields = ('created_at',)
    search_fields = ('method',)

class PaymentsCreateAPIView(CreateAPIView):
    """
    Создание платежа
    """
    serializer_class = PaymentCreateSerializer
    queryset = Payment.objects.all()

    def create(self, request, *args, **kwargs):
        if request.data.get('course'):
            request.data['cost'] = 4000
        else:
            request.data['cost'] = 1000
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        if serializer.instance.course:
            name = serializer.instance.course.title
        else:
            name = serializer.instance.lesson.title
        if serializer.instance.method == 'card':
            strike_product = create_product(name)
            price = serializer.instance.cost
            price_id = create_price(strike_product.id, price)
            session = create_checkout_session(price_id.id)
            serializer.instance.session_id = session.id
            serializer.instance.payment_link = session.url
            serializer.save()
        else:
            serializer.save()
