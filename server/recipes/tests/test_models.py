from django.test import TestCase
from django.contrib.auth.models import User
from recipes.models import Recipe, Ingredient

class RecipeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='modeltest', password='pass')
        self.recipe = Recipe.objects.create(
            user=self.user,
            title='Test Recipe',
            description='Just testing',
            instructions='Mix well'
        )

    def test_recipe_str_returns_title(self):
        self.assertEqual(str(self.recipe), 'Test Recipe')

    def test_recipe_belongs_to_user(self):
        self.assertEqual(self.recipe.user.username, 'modeltest')


class IngredientModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='inguser', password='pass')
        self.recipe = Recipe.objects.create(
            user=self.user,
            title='Ingredient Test Recipe',
            instructions='Cook stuff'
        )
        self.ingredient = Ingredient.objects.create(
            recipe=self.recipe,
            name='Flour',
            quantity='2',
            unit='cups'
        )

    def test_ingredient_str(self):
        self.assertEqual(str(self.ingredient), '2 cups Flour')

    def test_ingredient_links_to_recipe(self):
        self.assertEqual(self.ingredient.recipe, self.recipe)
