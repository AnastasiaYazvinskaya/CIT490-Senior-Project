from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.core.validators import RegexValidator

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'privacy', 'kkal', 'proteins', 'fats', 'carbohydrates', 'mealType', 'description', 'recommends') 
        widgets = {
            'description': forms.Textarea(attrs={'rows':5}),
            'recommends': forms.Textarea(attrs={'rows':5}),
        }


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('product_name', 'amount', 'unitType')
        