from django.urls import path
from . import views

urlpatterns = [
    path('recipes/', views.recipes, name='recipes'),
    path('recipes/card/<int:pk>/', views.recipe, name='recipe'),
    path('recipes/create/', views.create_update_recipe, name='create_recipe'),
    path('recipes/<int:pk>/update/', views.create_update_recipe, name='update_recipe'),
    #path('calculate_cpfc/<int:pk>/', views.calculate_cpfc, name='calculate_cpfc'),
    #path('dairy/', views.food_dairy, name='food_dairy'),
]