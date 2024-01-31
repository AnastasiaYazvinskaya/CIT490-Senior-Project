from django.forms import modelformset_factory
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# recipes page
@login_required
def recipes(request):
    recipes = Recipe.objects.filter(author = request.user)
        
    # Получение значения из поля поиска
    search = request.GET.get('searchrecipe')
    if search:
        # Фильтрация списка
        recipes = recipes.filter(name__icontains = search)#|recipes.filter(mealType__name__icontains = search)
    return render(request, 'recipes.html', {'recipes': recipes, 'search': search, 'activeRecipe': True})

# recipe page
@login_required
def recipe(request, pk=None):
    if pk:
        recipe = Recipe.objects.get(pk=pk)
        ingredients = Ingredient.objects.filter(recipe = recipe)
        return render(request, 'recipe_read.html', {'recipe': recipe, 'ingredients': ingredients, 'activeRecipe': True})
    return redirect('recipes')

# Create/Edit recipe page
@login_required
def create_update_recipe(request, pk=None):
    if pk != None:
        # Если ключ передан, то ищем объект
        recipeObj = Recipe.objects.get(pk = pk)
        ingredients = Ingredient.objects.filter(recipe = recipeObj)
    else: 
        # Если ключ не передан, то работаем с пустым объектом
        recipeObj = None
        ingredients = Ingredient.objects.none()
    if ingredients != None and len(ingredients) != 0:
        extra = 0
    else: extra = 1
    if request.method == "POST":
        recipeForm = RecipeForm(request.POST, request.FILES, instance = recipeObj)
        ingredientFormset = modelformset_factory(Ingredient, form=IngredientForm, extra=extra, can_delete=True)
        formset = ingredientFormset(request.POST, queryset=ingredients)
        if recipeForm.is_valid() and formset.is_valid():
            # Предсохраняем данные введенные с формы (но не вносим в базу)
            recipe = recipeForm.save(commit=False)
            if recipe.author is None:
                recipe.author = request.user
            # Переносим все изменения в базу
            recipe.save()
            for form in formset:
                ingredient = form.save(commit=False)
                if ingredient.product != None:
                    if ingredient.recipe is None:
                        ingredient.recipe = recipe
                    ingredient.save()
            for form in formset.deleted_forms:
                ingredient = form.save(commit=False)
                ingredient.delete()
                pass
            #form.save_m2m()
            return redirect('recipes')
    else:
        recipeForm = RecipeForm(instance = recipeObj)
        ingredientFormset = modelformset_factory(Ingredient, form=IngredientForm, extra=extra, can_delete=True)
        formset = ingredientFormset(queryset=ingredients)
    products = Product.objects.all()[:10]
    return render(request, "recipe_create_update.html", {'form': recipeForm, 'formset': formset, 'products': products, 'pk': pk, 'activeRecipe': True})