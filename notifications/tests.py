from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch


User = get_user_model()


class SendTelegramNotificationTest(APITestCase):
    def setUp(self):
        # Создаем пользователя для аутентификации
        self.user = User.objects.create_user(
            email="testuser@example.com", password="password"
        )
        self.client.force_authenticate(user=self.user)

        # URL эндпоинта
        self.url = "/notifications/send/"

    @patch("requests.post")
    def test_send_notification_success(self, mock_post):
        # Мокаем ответ от Telegram API
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "ok": True,
            "result": {
                "message_id": 123,
                "chat": {"id": 456, "type": "private", "username": "username"},
                "date": 1597512345,
                "text": "Текст сообщения",
            },
        }

        data = {"chat_id": "123456", "message": "Hello from the test"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["ok"], True)
        self.assertEqual(response.data["result"]["text"], "Текст сообщения")

    @patch("requests.post")
    def test_send_notification_failure(self, mock_post):
        # Мокаем ответ от Telegram API
        mock_post.return_value.status_code = 500

        data = {"chat_id": "123456", "message": "Hello from the test"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(
            response.data["error"], "Ошибка при отправке сообщения в Telegram"
        )

    def test_send_notification_missing_fields(self):
        data = {"chat_id": "123456"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"],
                         "chat_id и message обязательны")

        data = {"message": "Hello from the test"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"],
                         "chat_id и message обязательны")
