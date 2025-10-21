from django.test import TestCase
from django.contrib.auth.models import User
from recipes.models import Recipe, Ingredient
from recipes.serializers import RecipeSerializer, IngredientSerializer

class RecipeSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='seruser', password='pass')
        self.recipe = Recipe.objects.create(
            user=self.user,
            title='Serializer Test',
            instructions='Bake it'
        )
        Ingredient.objects.create(recipe=self.recipe, name='Egg', quantity='2', unit='pcs')

    def test_recipe_serializer_includes_ingredients(self):
        serializer = RecipeSerializer(self.recipe)
        data = serializer.data
        self.assertEqual(data['title'], 'Serializer Test')
        self.assertEqual(len(data['ingredients']), 1)
        self.assertEqual(data['ingredients'][0]['name'], 'Egg')


class IngredientSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='serializertest', password='pass')
        self.recipe = Recipe.objects.create(user=self.user, title='Serialize Me', instructions='...')
        self.ingredient = Ingredient.objects.create(recipe=self.recipe, name='Butter', quantity='2', unit='tbsp')

    def test_ingredient_serializer_fields(self):
        serializer = IngredientSerializer(self.ingredient)
        data = serializer.data
        self.assertEqual(data['name'], 'Butter')
        self.assertEqual(data['quantity'], '2')
        self.assertIn('recipe', data)
        self.assertEqual(data['recipe'], self.recipe.id)