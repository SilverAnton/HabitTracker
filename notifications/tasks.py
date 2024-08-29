from celery import shared_task

from .models import Notification
from habits.models import Habit
import requests
from django.conf import settings
from django.utils import timezone


@shared_task
def send_reminders():
    now = timezone.now()
    current_time = now.time()  # Текущее время

    # Фильтруем привычки по периодичности и времени напоминания
    habits = Habit.objects.filter(period=1, reminder_time=current_time)
    for habit in habits:
        chat_id = (
            habit.user.telegram_chat_id
        )
        message = f"Напоминание: {habit.action} в {habit.place} в {habit.time}."
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}

        # Отправляем уведомление
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            # Создаем запись о уведомлении в базе данных
            Notification.objects.create(
                user=habit.user, habit=habit, message=message, is_sent=True
            )
        else:
            # Создаем запись о уведомлении, если оно не было отправлено
            Notification.objects.create(
                user=habit.user, habit=habit, message=message, is_sent=False
            )
