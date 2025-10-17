from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    instructions = models.TextField()
    source_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=200)
    quantity = models.CharField(max_length=50, blank=True)  # e.g. "2 cups"
    unit = models.CharField(max_length=50, blank=True)      # optional
    is_checked = models.BooleanField(default=False)         # for grocery list functionality

    def __str__(self):
        # Displays nicely in the admin panel
        qty_part = f"{self.quantity} " if self.quantity else ""
        unit_part = f"{self.unit} " if self.unit else ""
        return f"{qty_part}{unit_part}{self.name}".strip()