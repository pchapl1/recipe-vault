from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class LoginAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='loginuser', password='Password123!')
        self.url = reverse('token_obtain_pair')

    def test_login_success(self):
        data = {"username": "loginuser", "password": "Password123!"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_fails_with_wrong_password(self):
        data = {"username": "loginuser", "password": "WrongPass"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
