from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from materials.models import Course, Lesson, Subscribe
from materials.paginators import MaterialsPagination
from materials.permissions import IsModerator, IsOwner
from materials.serializers import CourseSerializer, LessonSerializer, SubscribeSerializer
from materials.tasks import update_course


@method_decorator(
    name='create',
    decorator=swagger_auto_schema(
        operation_description='Создание курса')
)
@method_decorator(
    name='update',
    decorator=swagger_auto_schema(
        operation_description='Редактирование курса')
)
@method_decorator(
    name='partial_update',
    decorator=swagger_auto_schema(
        operation_description='Частичное редактирование курса')
)
@method_decorator(
    name='destroy',
    decorator=swagger_auto_schema(
        operation_description='Удаление курса')
)
@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        operation_description='Список курсов')
)
@method_decorator(
    name='retrieve',
    decorator=swagger_auto_schema(
        operation_description='Просмотр курса')
)
class CourseViewSet(viewsets.ModelViewSet):
    """
    CRUD для курсов
    """
    queryset = Course.objects.all().order_by('id')
    serializer_class = CourseSerializer
    pagination_class = MaterialsPagination

    def get_permissions(self):
        """
        Переопределение прав доступа
        """
        if self.action in ['update', 'partial_update']:
            permission_classes = [IsAdminUser | IsOwner | IsModerator]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser | IsOwner]
        elif self.action == 'retrieve' or self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Переопределение метода создания курса
        Добавление владельца курса (текущий пользователь)
        """
        serializer.save(owner=self.request.user)


    def perform_update(self, serializer):
        """
        Переопределение метода обновления курса
        """
        # Отправка задачи на обновление подписок: если курс обновлен, то отправляется уведомление
        update_course.delay(
            course_id=serializer.instance.id,
            message=f'Общее обновление курса!'
            )
        serializer.save()


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Создание урока: POST /lessons/create/
    Создание от имени текущего пользователя
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        update_course.delay(
            course_id=serializer.instance.course.id,
            message=f'Добавлен новый урок: {serializer.instance}'
        )
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """
    Список уроков: GET /lessons/
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    pagination_class = MaterialsPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Просмотр урока: GET /lessons/<int:pk>/
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser | IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Редактирование урока: PATCH /lessons/<int:pk>/update/
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser | IsOwner | IsModerator]

    def perform_update(self, serializer):
        # Отправка задачи на обновление подписок: если урок обновлен, то отправляется уведомление
        update_course.delay(
            course_id=serializer.instance.course.id,
            message=f'Урок {serializer.instance} обновлен'
        )
        serializer.save()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Удаление урока: DELETE /lessons/<int:pk>/delete/
    """
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser | IsOwner]


class SubscribeAPIView(generics.CreateAPIView):
    """
    Подписка на курс: POST /courses/subscribe_toggle/

    Если подписка уже существует, то она удаляется, иначе создается
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SubscribeSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course')
        course = get_object_or_404(Course, id=course_id)
        check = Subscribe.objects.filter(user=user, course=course).exists()
        if check:
            # delete subscribe
            Subscribe.objects.filter(user=user, course=course).delete()
            message = 'Подписка удалена'
            st = status.HTTP_204_NO_CONTENT
        else:
            # create subscribe
            Subscribe.objects.create(user=user, course=course)
            message = 'Подписка создана'
            st = status.HTTP_201_CREATED
        return Response({'message': message}, status=st)


class SuccessPaymentTemplateView(TemplateView):
    """
    Шаблон страницы успешной оплаты
    """
    template_name = 'materials/success_payment.html'


class CancelPaymentTemplateView(TemplateView):
    """
    Шаблон страницы отмены оплаты
    """
    template_name = 'materials/cancel_payment.html'