from rest_framework import viewsets, permissions

from drf_yasg.utils import swagger_auto_schema

from .models import Habit
from .paginations import HabitPagination
from .serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.query_params.get("public"):
                return Habit.objects.filter(is_public=True)
            return Habit.objects.filter(user=self.request.user)
        return Habit.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Создание новой привычки для текущего пользователя.",
        request_body=HabitSerializer,
        responses={
            201: HabitSerializer,
            400: "Некорректные данные.",
        },
    )
    def create(self, request, *args, **kwargs):
        """Создать новую привычку"""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить список привычек для текущего пользователя или публичных привычек.",
        responses={
            200: HabitSerializer(many=True),
        },
    )
    def list(self, request, *args, **kwargs):
        """Список привычек"""
        return super().list(request, *args, **kwargs)
