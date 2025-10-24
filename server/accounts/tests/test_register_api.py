from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class RegisterAPITests(APITestCase):
    def test_register_new_user_success(self):
        url = reverse('register')
        data = {"username": "testuser", "email": "test@example.com", "password": "Password123!"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertTrue(User.objects.filter(username='testuser').exists())
