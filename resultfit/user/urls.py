from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/trainer/', views.trainer_register, name='trainer_register'),
    path('register/trainer/<str:code>', views.trainer_register, name='trainer_register_by_code'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('reset/', views.reset_password, name='reset'),
    
    path('profile/', views.profile, name='profile'),
    path('home/', views.home, name='home'),

    path('trainers/', views.trainers, name='trainers'),
    path('trainers/card/<int:pk>/', views.trainer, name='trainer'),
    path('trainers/create/', views.create_update_trainer, name='create_trainer'),
    path('trainers/<int:pk>/update/', views.create_update_trainer, name='update_trainer'),
    #path('trainers/<int:pk>/delete/', views.delete_trainer, name='delete_trainer'),
    
    path('register/trainer/validate_code/', views.validate_code, name='validate_code'),
    path('trainers/send_email/', views.send_email, name='send_email_table'),
]