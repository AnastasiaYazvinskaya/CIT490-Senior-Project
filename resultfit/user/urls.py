from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('reset/', views.reset_password, name='reset'),
    
    path('profile/', views.profile, name='profile'),
    path('profile/<int:pk>/update/', views.update_profile, name='update_profile'),
    path('home/', views.home, name='home'),
    path('home/choose_trainer/', views.choose_trainer, name='choose_trainer'),
]