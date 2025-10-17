from django.test import TestCase
from django.contrib import admin
from recipes.models import Recipe, Ingredient

class AdminRegistrationTests(TestCase):
    def test_recipe_model_registered_in_admin(self):
        self.assertIn(Recipe, admin.site._registry)

    def test_ingredient_model_registered_in_admin(self):
        self.assertIn(Ingredient, admin.site._registry)
