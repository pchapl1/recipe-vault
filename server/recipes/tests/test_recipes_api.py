from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from recipes.models import Recipe

class RecipeAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_recipe(self):
        url = reverse('recipe-list')
        data = {
            'title': 'Pancakes',
            'description': 'Fluffy pancakes',
            'instructions': 'Mix and cook',
            'image_url': '',
            'source_url': ''
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Recipe.objects.get().title, 'Pancakes')
