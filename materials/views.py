from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from materials.models import Course, Lesson
from materials.permissions import IsModerator, IsOwner
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            permission_classes = [IsAdminUser | IsOwner | IsModerator]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser | IsOwner]
        elif self.action == 'retrieve':
            permission_classes = [IsAdminUser | IsOwner | IsModerator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        request.data["owner"] = request.user.pk
        data = super().create(request=request, *args, **kwargs)
        return data

    def get_queryset(self):
        data = super().get_queryset()
        if self.request.user.is_superuser or self.request.user.groups.filter(name='moderator').exists():
            return data
        return data.filter(owner=self.request.user)




class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def create(self, request, *args, **kwargs):
        request.data["owner"] = request.user.pk
        data = super().create(request=request, *args, **kwargs)
        return data


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        data = super().get_queryset()
        if self.request.user.is_superuser or self.request.user.groups.filter(name='moderator').exists():
            return data
        return data.filter(owner=self.request.user)

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser | IsOwner | IsModerator]

class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser | IsOwner | IsModerator]

class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser | IsOwner]
