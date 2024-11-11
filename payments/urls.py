from django.urls import path

from payments.apps import PaymentsConfig
from payments.views import PaymentsListAPIView, PaymentsCreateAPIView

app_name = PaymentsConfig.name

urlpatterns = [
    path('', PaymentsListAPIView.as_view(), name='payment_list'),
    path('create/', PaymentsCreateAPIView.as_view(), name='payment_create')
]
