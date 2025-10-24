from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class AuthAPITests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            "username": "testuser",
            "password": "password123",
            "email": "test@example.com"
        }

    def test_register_creates_user_and_returns_tokens(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('access_expires', response.data)
        self.assertIn('refresh_expires', response.data)
        self.assertEqual(response.data['user']['username'], self.user_data['username'])

    def test_login_returns_tokens_and_expiration(self):
        # First, register a user
        User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password']
        )

        # Then login
        response = self.client.post(self.login_url, {
            "username": self.user_data['username'],
            "password": self.user_data['password']
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('access_expires', response.data)
        self.assertIn('refresh_expires', response.data)
        self.assertEqual(response.data['user']['username'], self.user_data['username'])

    def test_login_fails_with_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            "username": "wronguser",
            "password": "wrongpass"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user_data = {
            "username": "logoutuser",
            "password": "password123",
            "email": "logout@example.com"
        }
        # Create user and get tokens
        self.client.post(self.register_url, self.user_data, format='json')
        login_response = self.client.post(self.login_url, {
            "username": self.user_data['username'],
            "password": self.user_data['password']
        }, format='json')
        self.refresh = login_response.data['refresh']
        self.access = login_response.data['access']

    def test_logout_blacklists_refresh_token(self):
        response = self.client.post(
            self.logout_url,
            {"refresh": self.refresh},
            HTTP_AUTHORIZATION=f'Bearer {self.access}',
            format='json'
        )
        self.assertEqual(response.status_code, 205)
        self.assertEqual(response.data['detail'], 'Successfully logged out.')
