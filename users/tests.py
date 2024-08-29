from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserAPITests(APITestCase):
    def setUp(self):
        # URL для регистрации
        self.create_url = reverse("users:register")
        # URL для списка пользователей
        self.list_url = reverse("users:user-list")
        # URL для получения пользователя
        self.retrieve_url = lambda user_id: reverse(
            "users:user-detail", args=[user_id])
        # URL для обновления пользователя
        self.update_url = lambda user_id: reverse(
            "users:user-detail", args=[user_id])
        # URL для удаления пользователя
        self.delete_url = lambda user_id: reverse(
            "users:user-detail", args=[user_id])

    def test_create_user(self):
        data = {
            "email": "newuser@example.com",
            "password": "newpassword",
        }
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "newuser@example.com")

    def test_list_users(self):
        User.objects.create_user(
            email="user1@example.com", password="password")
        User.objects.create_user(
            email="user2@example.com", password="password")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_user(self):
        user = User.objects.create_user(
            email="user@example.com", password="password")
        response = self.client.get(self.retrieve_url(user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "user@example.com")

    def test_update_user(self):
        user = User.objects.create_user(
            email="user@example.com", password="password")
        data = {"email": "updateduser@example.com", "password": "newpassword"}
        response = self.client.patch(
            self.update_url(user.id), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.email, "updateduser@example.com")

    def test_delete_user(self):
        user = User.objects.create_user(
            email="user@example.com", password="password")
        response = self.client.delete(self.delete_url(user.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
