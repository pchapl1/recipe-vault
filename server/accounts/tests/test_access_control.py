from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class AccessControlTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="secureuser", password="Password123!")
        login_url = reverse('token_obtain_pair')
        token_response = self.client.post(login_url, {"username": "secureuser", "password": "Password123!"})
        self.token = token_response.data['access']
        self.recipe_url = reverse('recipe-list')  # update if different

    def test_protected_endpoint_denied_without_token(self):
        response = self.client.get(self.recipe_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_protected_endpoint_granted_with_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.recipe_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
