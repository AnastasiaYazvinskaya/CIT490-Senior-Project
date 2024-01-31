from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.core.validators import RegexValidator

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'privacy', 'kkal', 'proteins', 'fats', 'carbohydrates', 'mealType', 'description') 


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('product', 'amount', 'unitType')
        