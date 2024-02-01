from django.urls import path
from . import views

urlpatterns = [
    path('recipes/', views.recipes, name='recipes'),
    path('recipes/card/<int:pk>/', views.recipe, name='recipe'),
    path('recipes/create/', views.create_update_recipe, name='create_recipe'),
    path('recipes/<int:pk>/update/', views.create_update_recipe, name='update_recipe'),
    
    #path('recipes/create/update_datalist/', views.update_datalist, name='update_datalist'),
    #path('recipes/<int:pk>/update/update_datalist/', views.update_datalist, name='update_datalist'),
]