from rest_framework.routers import DefaultRouter

from materials.urls import urlpatterns
from users.apps import UsersConfig
from users.views import UserViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"", UserViewSet, basename='users')

urlpatterns = router.urls
