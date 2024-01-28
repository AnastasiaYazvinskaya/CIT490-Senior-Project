from django.contrib import admin
from .models import *

class IngredientInline(admin.StackedInline):
    model = Ingredient
    extra = 0

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'product', 'weight', 'weight_type')
admin.site.register(Ingredient, IngredientAdmin)

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'privacy')
    inlines = [IngredientInline]
admin.site.register(Recipe, RecipeAdmin)
