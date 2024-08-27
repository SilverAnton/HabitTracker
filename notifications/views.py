from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import requests


class SendTelegramNotification(APIView):
    def post(self, request):
        token = settings.TELEGRAM_BOT_TOKEN
        chat_id = request.data.get('chat_id')
        message = request.data.get('message')

        url = f'https://api.telegram.org/bot{token}/sendMessage'
        payload = {'chat_id': chat_id, 'text': message}
        response = requests.post(url, data=payload)
        return Response(response.json())
