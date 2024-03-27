from django.urls import path
from . import views

urlpatterns = [
    path('sport/', views.sport, name='sport'),
    path('sport/plan/', views.sport_plan, name='sport_plan'),
    path('sport/plan/<int:pk>', views.sport_plan_read, name='sport_plan_read'),
    path('sport/plan/<int:week>/create', views.sport_plan_create_update, name='sport_plan_create'),
    path('sport/plan/<int:pk>/update', views.sport_plan_create_update, name='sport_plan_update'),
    
    path('sport/day/<str:day>/', views.sport, name='sport_plan_by_date'),
    path('sport/choose_trainer/', views.choose_trainer, name='choose_trainer'),

    path('sport/plan/<int:week>/<int:client>/create', views.sport_plan_create_update, name='sport_plan_create_trainer'),
    path('sport/plan/<int:pk>/<int:client>/update', views.sport_plan_create_update, name='sport_plan_update_trainer'),
]