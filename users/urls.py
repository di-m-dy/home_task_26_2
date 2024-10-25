from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.urls import urlpatterns
from users.apps import UsersConfig
from users.views import UserViewSet, PaymentsListAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"", UserViewSet, basename='users')

urlpatterns = [
    path('payments/', PaymentsListAPIView.as_view(), name='payment_list'),
] + router.urls
