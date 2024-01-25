from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.clients, name='clients'),
    path('clients/card/<int:pk>/', views.client, name='client'),
    #path('dairy/', views.food_dairy, name='food_dairy'),
]