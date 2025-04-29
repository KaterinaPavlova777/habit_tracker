from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        super().setUp()

        self.user = User.objects.create_user(
            username='test',
            password='test123'
        )
        self.client.force_authenticate(user=self.user)

        self.habitU1 = Habit.objects.create(
            user=self.user,
            place="test01",
            time="11:52:00",
            action="Drink water",
            pleasant=False,
            periodicity="day",
            reward=None,
            lead_time="00:02:00",
            is_public=False
        )

        self.habitU2 = Habit.objects.create(
            user=self.user,
            place="test01",
            time="11:52:00",
            action="Stretching",
            pleasant=True,
            periodicity="day",
            reward=None,
            lead_time="00:01:30",
            is_public=True
        )

    def test_HabitList(self):
        response = self.client.get('/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['action'], "Stretching")

    def test_HabitCreate(self):
        data = {
            "place": "Home",
            "time": "12:00:00",
            "action": "Meditate",
            "pleasant": False,
            "periodicity": "day",
            "reward": "Chocolate",
            "lead_time": "00:01:00",
            "is_public": True
        }
        response = self.client.post('/habits/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        habit = Habit.objects.filter(action="Meditate").first()
        self.assertIsNotNone(habit)
        self.assertEqual(habit.user, self.user)

    def test_HabitCreate_validation(self):
        invalid_data = {
            "place": "Home",
            "time": "12:00:00",
            "action": "Invalid Habit",
            "pleasant": False,
            "periodicity": "day",
            "related": self.habitU2.id,
            "reward": "Chocolate",
            "lead_time": "00:03:00",
            "is_public": True
        }
        invalid_data2 = {
            "place": "Home",
            "time": "12:00:00",
            "action": "Invalid Habit",
            "pleasant": False,
            "periodicity": "day",
            "related": self.habitU1.id,
            "lead_time": "00:02:00",
            "is_public": True
        }
        response = self.client.post('/habits/create/', invalid_data)
        response2 = self.client.post('/habits/create/', invalid_data2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.json()
        errors2 = response2.json()
        print(errors2)

        self.assertIn("Время выполнения не должно превышать 0:02:00.", errors["non_field_errors"])
        self.assertIn("Разрешёно только выбрать связанную привычку или вознаграждение", errors["non_field_errors"])
        self.assertIn("Можно связывать только полезные с приятными привычками", errors2["non_field_errors"])

    def test_HabitUpdate(self):
        updated_data = {
            "place": "Updated Place",
            "time": "13:00:00",
            "action": "Updated Action",
            "pleasant": True,
            "periodicity": "2 days",
            "reward": '',
            "lead_time": "00:01:00",
            "is_public": False
        }
        response = self.client.put(f'/habits/update/{self.habitU1.id}', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        habit = Habit.objects.get(id=self.habitU1.id)
        self.assertEqual(habit.place, "Updated Place")
        self.assertEqual(habit.action, "Updated Action")

    def test_HabitDestroy(self):
        response = self.client.delete(f'/habits/delete/{self.habitU1.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_HabitDetail(self):
        response = self.client.get(f'/habits/detail/{self.habitU2.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data['action'], "Stretching")
        self.assertEqual(data['is_public'], True)
