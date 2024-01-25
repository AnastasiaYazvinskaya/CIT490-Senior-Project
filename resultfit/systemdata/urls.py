from django.urls import path
from . import views

urlpatterns = [
    path('', views.systemdata, name='systemdata'),
    path('activity/', views.activity, name='activity'),
    path('activity/create/', views.create_update_activity, name='create_activity'),
    path('activity/<int:pk>/update/', views.create_update_activity, name='update_activity'),
    path('activity/<int:pk>/delete/', views.delete_activity, name='delete_activity'),
    
    path('purpose/', views.purpose, name='purpose'),
    path('purpose/create/', views.create_update_purpose, name='create_purpose'),
    path('purpose/<int:pk>/update/', views.create_update_purpose, name='update_purpose'),
    path('purpose/<int:pk>/delete/', views.delete_purpose, name='delete_purpose'),
]