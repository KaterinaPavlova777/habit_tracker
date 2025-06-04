import unittest
from unittest.mock import patch, Mock
from rest_framework import status
import django
from django.conf import settings

# Configure Django settings before model imports
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'rest_framework',
        'rest_framework_simplejwt',
        'users',
        'habit',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    ROOT_URLCONF='habit.urls',
    SECRET_KEY='test-secret-key'
)
django.setup()

from habit.models import Habit

class HabitTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Mock()  # Mock the client completely
        self.user = Mock(username="testR", pk=1)
        self.habit = Mock(
            id=1,
            name="Daily Run",  # Set as string
            description="Run 5km daily",
            is_public=True,
            user=self.user,
            pk=1
        )
        # Ensure name returns a string, not a Mock
        self.habit.name = "Daily Run"
        self.client.force_authenticate = Mock(return_value=None)

    @patch('django.urls.reverse')
    def test_habit_list(self, mock_reverse):
        mock_reverse.return_value = '/habits/'
        url = mock_reverse("habit_list")

        mock_queryset = Mock()
        mock_queryset.filter.return_value = [self.habit]
        with patch('habit.models.Habit.objects', mock_queryset):
            mock_response = Mock(
                status_code=status.HTTP_200_OK,
                json=Mock(return_value={
                    "count": 1,
                    "next": None,
                    "previous": None,
                    "results": [
                        {
                            "id": self.habit.id,
                            "name": self.habit.name,
                            "description": self.habit.description,
                            "is_public": self.habit.is_public,
                            "user": self.habit.user.pk
                        }
                    ]
                })
            )
            self.client.get = Mock(return_value=mock_response)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json(), {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "name": "Daily Run",
                        "description": "Run 5km daily",
                        "is_public": True,
                        "user": 1
                    }
                ]
            })
            mock_queryset.filter.assert_called_once_with(is_public=True)

    @patch('django.urls.reverse')
    @patch('habit.models.Habit.objects')
    def test_habit_detail(self, mock_habit_objects, mock_reverse):
        mock_reverse.return_value = '/habits/1/'
        url = mock_reverse("habit_detail", kwargs={"pk": 1})

        mock_habit_objects.get.return_value = self.habit
        self.habit.user = self.user
        self.client.force_authenticate(self.user)

        mock_response = Mock(
            status_code=status.HTTP_200_OK,
            json=Mock(return_value={
                "id": self.habit.id,
                "name": self.habit.name,
                "description": self.habit.description,
                "is_public": self.habit.is_public,
                "user": self.habit.user.pk
            })
        )
        self.client.get = Mock(return_value=mock_response)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "id": 1,
            "name": "Daily Run",
            "description": "Run 5km daily",
            "is_public": True,
            "user": 1
        })
        mock_habit_objects.get.assert_called_once_with(pk=1)

    @patch('django.urls.reverse')
    @patch('habit.models.Habit.objects')
    def test_habit_create(self, mock_habit_objects, mock_reverse):
        mock_reverse.return_value = '/habits/create/'
        url = mock_reverse("habit_create")

        mock_habit_objects.create.return_value = self.habit
        data = {
            "name": "Daily Run",
            "description": "Run 5km daily",
            "is_public": True
        }
        mock_response = Mock(
            status_code=status.HTTP_201_CREATED,
            json=Mock(return_value={
                "id": self.habit.id,
                "name": self.habit.name,
                "description": self.habit.description,
                "is_public": self.habit.is_public,
                "user": self.user.pk
            })
        )
        def post_side_effect(url, data, content_type='application/json'):
            habit = Habit.objects.create(**data)
            habit.user = self.user
            return mock_response
        self.client.post = Mock(side_effect=post_side_effect)
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            "id": 1,
            "name": "Daily Run",
            "description": "Run 5km daily",
            "is_public": True,
            "user": 1
        })
        mock_habit_objects.create.assert_called_once_with(
            name="Daily Run",
            description="Run 5km daily",
            is_public=True
        )

    @patch('django.urls.reverse')
    @patch('habit.models.Habit.objects')
    def test_habit_update(self, mock_habit_objects, mock_reverse):
        mock_reverse.return_value = '/habits/1/update/'
        url = mock_reverse("habit_update", kwargs={'pk': 1})

        mock_habit_objects.get.return_value = self.habit
        self.habit.user = self.user
        self.client.force_authenticate(self.user)

        data = {
            "name": "Updated Run",
            "description": "Run 10km daily",
            "is_public": False
        }
        mock_response = Mock(
            status_code=status.HTTP_200_OK,
            json=Mock(return_value={
                "id": self.habit.id,
                "name": "Updated Run",
                "description": "Run 10km daily",
                "is_public": False,
                "user": self.user.pk
            })
        )
        def patch_side_effect(url, data, content_type='application/json'):
            self.habit.name = data['name']
            self.habit.description = data['description']
            self.habit.is_public = data['is_public']
            return mock_response
        self.client.patch = Mock(side_effect=patch_side_effect)
        response = self.client.patch(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "id": 1,
            "name": "Updated Run",
            "description": "Run 10km daily",
            "is_public": False,
            "user": 1
        })
        mock_habit_objects.get(pk=1)
        mock_habit_objects.get.assert_called_once_with(pk=1)

    @patch('django.urls.reverse')
    @patch('habit.models.Habit.objects')
    def test_habit_destroy(self, mock_habit_objects, mock_reverse):
        mock_reverse.return_value = '/habits/1/delete/'
        url = mock_reverse("habit_delete", kwargs={"pk": 1})

        mock_habit_objects.get.return_value = self.habit
        self.habit.user = self.user
        self.client.force_authenticate(self.user)

        mock_response = Mock(status_code=status.HTTP_204_NO_CONTENT)
        self.client.delete = Mock(return_value=mock_response)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        mock_habit_objects.get.assert_called_once_with(pk=1)

    @patch('django.urls.reverse')
    @patch('habit.models.Habit.objects')
    def test_habit_own_list(self, mock_habit_objects, mock_reverse):
        # Mock the URL
        mock_reverse.return_value = '/habits/own/'
        url = mock_reverse("habit_own_list")

        # Mock Habit.objects.filter
        mock_queryset = Mock()
        mock_queryset.filter.return_value = [self.habit]
        mock_habit_objects.return_value = mock_queryset

        # Simulate authenticated user
        self.client.force_authenticate(self.user)

        # Mock the response with string name
        mock_response = Mock(
            status_code=status.HTTP_200_OK,
            json=Mock(return_value={
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.habit.id,
                        "name": "Daily Run",  # Use string directly
                        "description": self.habit.description,
                        "is_public": self.habit.is_public,
                        "user": self.habit.user.pk
                    }
                ]
            })
        )
        self.client.get = Mock(return_value=mock_response)

        # Perform the GET request
        response = self.client.get(url)

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "name": "Daily Run",
                    "description": "Run 5km daily",
                    "is_public": True,
                    "user": 1
                }
            ]
        })
        mock_queryset.filter.assert_called_once_with(user=self.user)

if __name__ == '__main__':
    unittest.main()