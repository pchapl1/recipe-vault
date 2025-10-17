from rest_framework import serializers
from .models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'quantity', 'unit', 'is_checked', 'recipe']



class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'image_url',
            'instructions',
            'source_url',
            'created_at',
            'updated_at',
            'ingredients',
        ]
