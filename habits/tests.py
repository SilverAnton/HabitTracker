from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User
from .models import Habit


class HabitAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password",
        )
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            user=self.user,
            action="Morning Run",
            time="07:00",
            place="Park",
            is_pleasant=True,
            period=1,
            duration=30,
        )

    def test_create_habit(self):
        url = reverse("habits:habit-list")
        data = {
            "action": "Evening Walk",
            "time": "19:00",
            "place": "Neighborhood",
            "is_pleasant": True,
            "period": 1,
            "duration": 20,
        }

        response = self.client.post(url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)
        self.assertEqual(Habit.objects.last().action, "Evening Walk")

    def test_list_habits(self):
        url = reverse("habits:habit-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], "Morning Run")
        print(response.data)

    def test_retrieve_habit(self):
        url = reverse("habits:habit-detail", args=[self.habit.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "Morning Run")
        print(response.data)

    def test_update_habit(self):
        url = reverse("habits:habit-detail", args=[self.habit.id])
        data = {
            "action": "Morning Yoga",
            "time": "06:30",
            "place": "Home",
            "is_pleasant": True,
            "period": 1,
            "duration": 15,
        }

        response = self.client.put(url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Morning Yoga")

    def test_partial_update_habit(self):
        url = reverse("habits:habit-detail", args=[self.habit.id])
        data = {
            "action": "Morning Meditation",
        }

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Morning Meditation")
        print(response.data)

    def test_delete_habit(self):
        url = reverse("habits:habit-detail", args=[self.habit.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)
        print(response.data)
