from django.urls import path, re_path
from . import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('fooddairy/', views.fooddairy, name='fooddairy'),
    path('fooddairy/calculate_cpfc/<int:pk>/', views.calculate_cpfc, name='calculate_cpfc'),
    path('fooddairy/dairy/', views.food_dairy, name='food_dairy'),

    path('fooddairy/dairy/save_comment/', views.save_comment, name='save_comment'),
    path('fooddairy/dairy/save_note/', views.save_note, name='save_note'),
]
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }), ]