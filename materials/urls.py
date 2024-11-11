from django.urls import path
from rest_framework.routers import DefaultRouter
from materials.apps import MaterialsConfig
from materials.views import CourseViewSet, LessonCreateAPIView, LessonRetrieveAPIView, LessonListAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, SubscribeAPIView, SuccessPaymentTemplateView, CancelPaymentTemplateView

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename='courses')

urlpatterns = [
                  path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
                  path('lessons/', LessonListAPIView.as_view(), name='lesson_list'),
                  path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
                  path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson_update'),
                  path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
                  path('courses/subscribe_toggle/', SubscribeAPIView.as_view(), name='lesson_subscribe'),
                  path('success_payment/', SuccessPaymentTemplateView.as_view(), name='success_payment'),
                  path('cancel_payment/', CancelPaymentTemplateView.as_view(), name='cancel_payment'),

              ] + router.urls
