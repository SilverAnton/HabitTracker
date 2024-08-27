from django.urls import path

from .apps import NotificationsConfig
from .views import SendTelegramNotification

app_name = NotificationsConfig.name

urlpatterns = [
    path('send/', SendTelegramNotification.as_view(), name='send_telegram_notification'),
]