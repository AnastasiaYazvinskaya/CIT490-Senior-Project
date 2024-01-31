from django.contrib import admin
from .models import *

class IngredientInline(admin.StackedInline):
    model = Ingredient
    extra = 0

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'amount', 'unitType')
admin.site.register(Ingredient, IngredientAdmin)

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'privacy', 'mealType')
    inlines = [IngredientInline]
admin.site.register(Recipe, RecipeAdmin)
