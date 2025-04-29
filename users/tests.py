from rest_framework import status
from rest_framework.test import APITestCase


class UsersTestCase(APITestCase):

    def test_UserRegistration(self):
        data = {
            "username": "testR",
            "password": "test",
            "password_confirm": "test",
            "tg_chat_id": 919000287
        }
        response = self.client.post('/users/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['username'], 'testR')