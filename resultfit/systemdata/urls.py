from django.urls import path
from . import views

urlpatterns = [
    path('', views.systemdata, name='systemdata'),
    
    path('activity/', views.activity, name='activity'),
    path('activity/create/', views.create_update_activity, name='create_activity'),
    path('activity/<int:pk>/update/', views.create_update_activity, name='update_activity'),
    path('activity/<int:pk>/delete/', views.delete_activity, name='delete_activity'),
    path('activity/<int:pk>/activate/', views.activate_activity, name='activate_activity'),
    
    path('purpose/', views.purpose, name='purpose'),
    path('purpose/create/', views.create_update_purpose, name='create_purpose'),
    path('purpose/<int:pk>/update/', views.create_update_purpose, name='update_purpose'),
    path('purpose/<int:pk>/delete/', views.delete_purpose, name='delete_purpose'),
    path('purpose/<int:pk>/activate/', views.activate_purpose, name='activate_purpose'),

    path('privacy/', views.privacy, name='privacy'),
    path('privacy/create/', views.create_update_privacy, name='create_privacy'),
    path('privacy/<int:pk>/update/', views.create_update_privacy, name='update_privacy'),
    path('privacy/<int:pk>/delete/', views.delete_privacy, name='delete_privacy'),
    path('privacy/<int:pk>/activate/', views.activate_privacy, name='activate_privacy'),

    path('unit/', views.unit, name='unit'),
    path('unit/create/', views.create_update_unit, name='create_unit'),
    path('unit/<int:pk>/update/', views.create_update_unit, name='update_unit'),
    path('unit/<int:pk>/delete/', views.delete_unit, name='delete_unit'),
    path('unit/<int:pk>/activate/', views.activate_unit, name='activate_unit'),

    path('product/', views.product, name='product'),
    path('product/create/', views.create_update_product, name='create_product'),
    path('product/<int:pk>/update/', views.create_update_product, name='update_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('product/<int:pk>/activate/', views.activate_product, name='activate_product'),

    path('reset/', views.reset, name='reset'),
    path('reset/update_table/', views.update_table, name='update_table'),
]