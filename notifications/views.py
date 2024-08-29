from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests


class SendTelegramNotification(APIView):

    @swagger_auto_schema(
        operation_description="Отправка уведомления в Telegram для указанного пользователя.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["chat_id", "message"],
            properties={
                "chat_id": openapi.Schema(
                    type=openapi.TYPE_STRING, description="ID чата Telegram"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Текст сообщения"
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Уведомление успешно отправлено.",
                examples={
                    "application/json": {
                        "ok": True,
                        "result": {
                            "message_id": 123,
                            "chat": {
                                "id": 456,
                                "type": "private",
                                "username": "username",
                            },
                            "date": 1597512345,
                            "text": "Текст сообщения",
                        },
                    }
                },
            ),
            400: "Неверные данные запроса.",
            500: "Ошибка при отправке сообщения.",
        },
    )
    def post(self, request):
        token = settings.TELEGRAM_BOT_TOKEN
        chat_id = request.data.get("chat_id")
        message = request.data.get("message")

        if not chat_id or not message:
            return Response(
                {"error": "chat_id и message обязательны"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Ошибка при отправке сообщения в Telegram"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
