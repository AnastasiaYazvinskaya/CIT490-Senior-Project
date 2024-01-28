from django.urls import path
from . import views

urlpatterns = [
    path('clients/<str:type>/', views.clients, name='clients'),
    path('clients/card/<int:pk>/', views.client, name='client'),
    path('accept_client/<int:pk>/', views.accept_client, name='accept_client'),
]