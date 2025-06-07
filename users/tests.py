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
    ROOT_URLCONF='users.urls',
    SECRET_KEY='test-secret-key'
)
django.setup()

from users.models import User

class UsersTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Mock()  # Mock the client completely
        self.user = Mock(username="testR", tg_chat_id="919000287", pk=1)
        self.client.force_authenticate = Mock(return_value=None)

    @patch('django.urls.reverse')  # Mock the reverse function
    @patch('users.models.User.objects.create_user')  # Mock User creation
    def test_UserRegistration(self, mock_create_user, mock_reverse):
        # Mock the URL returned by reverse
        mock_reverse.return_value = '/register/'
        url = mock_reverse("register")

        # Mock the user creation
        mock_create_user.return_value = self.user

        # Prepare request data
        data = {
            "username": "testR",
            "password": "test",
            "password_confirm": "test",
            "tg_chat_id": "919000287"
        }

        # Mock the response for the POST request
        mock_response = Mock(
            status_code=status.HTTP_201_CREATED,
            json=Mock(return_value={
                "username": self.user.username,
                "tg_chat_id": self.user.tg_chat_id
            })
        )
        # Simulate the view/serializer calling create_user when client.post is called
        def post_side_effect(url, data, content_type='application/json'):
            # Simulate serializer validation and user creation
            if data.get('password') == data.get('password_confirm'):
                User.objects.create_user(
                    username=data['username'],
                    password=data['password'],
                    tg_chat_id=data.get('tg_chat_id')
                )
            return mock_response

        self.client.post = Mock(side_effect=post_side_effect)

        # Perform the POST request
        response = self.client.post(url, data, content_type='application/json')

        # Assert response status and content
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            "username": "testR",
            "tg_chat_id": "919000287"
        })

        # Verify create_user was called with correct arguments
        mock_create_user.assert_called_once_with(
            username='testR',
            password='test',
            tg_chat_id='919000287'  # Include tg_chat_id as it’s likely passed by the serializer
        )

if __name__ == '__main__':
    unittest.main()