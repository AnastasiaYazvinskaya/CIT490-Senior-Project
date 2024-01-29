from django.urls import path
from . import views

urlpatterns = [
    path('recipes/', views.recipes, name='recipes'),
    #path('calculate_cpfc/<int:pk>/', views.calculate_cpfc, name='calculate_cpfc'),
    #path('dairy/', views.food_dairy, name='food_dairy'),
]