from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='start_page'),
    path('table/', views.table, name='table'),
    
]