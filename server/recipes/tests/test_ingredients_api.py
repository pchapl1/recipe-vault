from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from recipes.models import Recipe, Ingredient

class IngredientAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='apiuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.recipe = Recipe.objects.create(
            user=self.user,
            title='API Recipe',
            instructions='Do something'
        )

    def test_create_ingredient(self):
        url = reverse('ingredient-list')
        data = {
            'name': 'Sugar',
            'quantity': '1',
            'unit': 'cup',
            'is_checked': False,
            'recipe': self.recipe.id  # ✅ important!
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ingredient.objects.count(), 1)
        ingredient = Ingredient.objects.get()
        self.assertEqual(ingredient.name, 'Sugar')
        self.assertEqual(ingredient.recipe, self.recipe)

    def test_list_ingredients(self):
        Ingredient.objects.create(recipe=self.recipe, name='Salt', quantity='1', unit='tsp')
        url = reverse('ingredient-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_ingredient(self):
        ingredient = Ingredient.objects.create(recipe=self.recipe, name='Salt', quantity='1', unit='tsp')
        url = reverse('ingredient-detail', args=[ingredient.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Salt')

    def test_update_ingredient(self):
        ingredient = Ingredient.objects.create(recipe=self.recipe, name='Sugar', quantity='1', unit='cup')
        url = reverse('ingredient-detail', args=[ingredient.id])
        response = self.client.patch(url, {'is_checked': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertTrue(ingredient.is_checked)

    def test_delete_ingredient(self):
        ingredient = Ingredient.objects.create(recipe=self.recipe, name='Honey', quantity='2', unit='tbsp')
        url = reverse('ingredient-detail', args=[ingredient.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ingredient.objects.count(), 0)

