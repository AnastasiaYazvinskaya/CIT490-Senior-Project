from django.urls import path
from . import views

urlpatterns = [
    path('clients/<str:type>/', views.clients, name='clients'),
    path('clients/card/<int:pk>/data', views.client, name='client'),
    path('clients/card/<int:pk>/meal', views.client_meal, name='client_meal'),
    path('clients/card/<int:pk>/sport', views.client_sport, name='client_sport'),
    path('accept_client/<int:pk>/', views.accept_client, name='accept_client'),
]