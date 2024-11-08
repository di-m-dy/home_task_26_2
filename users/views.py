from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from users.models import User
from users.permissions import IsCurrentUser
from users.serializers import UserSerializer, UserCreateSerializer, UserListSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class UserListAPIView(ListAPIView):
    """
    Список пользователей
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Переопределение метода для возврата разных сериализаторов в зависимости от прав пользователя
        Если пользователь является суперпользователем, то возвращается полный сериализатор
        Если нет, то возвращается урезанный сериализатор
        """
        if self.request.user.is_superuser:
            return UserSerializer
        return UserListSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    """
    Получение пользователя
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Переопределение метода для возврата разных сериализаторов в зависимости от прав пользователя
        Если пользователь является суперпользователем или это его собственный профиль,
        то возвращается полный сериализатор
        """
        if self.request.user.pk == self.kwargs.get('pk') or self.request.user.is_superuser:
            return UserSerializer
        return UserListSerializer


class UserUpdateAPIView(UpdateAPIView):
    """
    Обновление пользователя
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsCurrentUser | IsAdminUser]


class UserDestroyAPIView(DestroyAPIView):
    """
    Удаление пользователя
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsCurrentUser | IsAdminUser]


class UserCreateAPIView(CreateAPIView):
    """
    Создание пользователя
    """
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password) # Хеширование пароля
        user.save()
