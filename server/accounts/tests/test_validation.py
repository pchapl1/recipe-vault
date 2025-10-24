from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class ValidationTests(APITestCase):
    def test_register_fails_with_missing_username(self):
        url = reverse('register')
        data = {"email": "missing@example.com", "password": "Password123!"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_fails_if_username_taken(self):
        User.objects.create_user(username="dupe", email="dupe@example.com", password="Password123!")
        url = reverse('register')
        data = {"username": "dupe", "email": "new@example.com", "password": "Password123!"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
