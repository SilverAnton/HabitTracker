from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Habit
from .serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.query_params.get('public'):
                return Habit.objects.filter(is_public=True)
            return Habit.objects.filter(user=self.request.user)
        return Habit.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
