from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Habit(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="habits")
    action = models.CharField(max_length=255)
    time = models.TimeField()
    place = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dependent_habits",
    )
    reward = models.CharField(max_length=255, null=True, blank=True)
    period = models.PositiveIntegerField(default=1)
    duration = models.PositiveIntegerField()
    is_public = models.BooleanField(default=False)
    reminder_time = models.TimeField(null=True, blank=True)

    def clean(self):
        if self.related_habit and self.reward:
            raise ValidationError(
                "Нельзя указывать одновременно и связанную привычку, и вознаграждение."
            )

        if self.duration is not None and self.duration > 120:
            raise ValidationError(
                "Время выполнения не должно превышать 120 секунд.")

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")

        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError(
                "Приятная привычка не может иметь вознаграждение или связанную привычку."
            )

        if self.period < 1 or self.period > 7:
            raise ValidationError(
                "Периодичность выполнения должна быть от 1 до 7 дней."
            )

    def __str__(self):
        return f"{self.action} at {self.time} in {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["time"]
