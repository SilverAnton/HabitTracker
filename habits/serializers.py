from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        # Валидация полей модели
        habit = Habit(**data)
        habit.clean()
        return data
