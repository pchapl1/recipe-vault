from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class TokenRefreshTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='refreshtest', password='Password123!')
        login_url = reverse('token_obtain_pair')
        login_response = self.client.post(login_url, {"username": "refreshtest", "password": "Password123!"})
        self.refresh_token = login_response.data['refresh']
        self.url = reverse('token_refresh')

    def test_refresh_token_works(self):
        response = self.client.post(self.url, {"refresh": self.refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
