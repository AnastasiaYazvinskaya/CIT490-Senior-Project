from django.urls import path, re_path
from . import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('fooddairy/', views.fooddairy, name='fooddairy'),
    path('fooddairy/day/<str:day>/', views.fooddairy, name='meal_plan_by_date'),
    path('fooddairy/calculate_cpfc/', views.calculate_cpfc, name='calculate_cpfc'),
    path('fooddairy/dairy/<str:day>/', views.food_dairy, name='food_dairy_by_date'),
    path('fooddairy/dairy/', views.food_dairy, name='food_dairy'),
    path('fooddairy/dairy/addNote/<int:meal>/', views.add_note, name='add_note'),
    path('fooddairy/meal/<int:pk>/', views.meal, name='meal'),

    path('fooddairy/dairy/save_comment/', views.save_comment, name='save_comment'),
    path('fooddairy/dairy/<str:day>/save_comment/', views.save_comment, name='save_comment_by_date'),
    path('clients/card/(?P\d+)/meal/save_comment/', views.save_comment, name='save_comment_by_date'),
    path('fooddairy/dairy/save_note/', views.save_note, name='save_note'),
    path('fooddairy/dairy/<str:day>/save_note/', views.save_note, name='save_note_by_date'),
]
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }), ]