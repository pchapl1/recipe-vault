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

    def test_list_recipes(self):
        Recipe.objects.create(user=self.user, title='Toast', instructions='Toast bread')
        url = reverse('recipe-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_recipe(self):
        recipe = Recipe.objects.create(user=self.user, title='Soup', instructions='Boil water')
        url = reverse('recipe-detail', args=[recipe.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Soup')

    def test_update_recipe(self):
        recipe = Recipe.objects.create(user=self.user, title='Pasta', instructions='Boil')
        url = reverse('recipe-detail', args=[recipe.id])
        response = self.client.patch(url, {'title': 'Pasta Updated'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, 'Pasta Updated')

    def test_delete_recipe(self):
        recipe = Recipe.objects.create(user=self.user, title='Salad', instructions='Mix')
        url = reverse('recipe-detail', args=[recipe.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 0)
