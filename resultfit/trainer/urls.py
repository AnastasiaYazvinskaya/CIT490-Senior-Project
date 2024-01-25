from django.urls import path
from . import views

urlpatterns = [
    path('register/trainer/', views.trainer_register, name='trainer_register'),
    path('register/trainer/<str:code>', views.trainer_register, name='trainer_register_by_code'),

    path('trainers/', views.trainers, name='trainers'),
    path('trainers/card/<int:pk>/', views.trainer, name='trainer'),
    path('trainers/create/', views.create_update_trainer, name='create_trainer'),
    path('trainers/<int:pk>/update/', views.create_update_trainer, name='update_trainer'),
    #path('trainers/<int:pk>/delete/', views.delete_trainer, name='delete_trainer'),
    
    path('register/trainer/validate_code/', views.validate_code, name='validate_code'),
    path('trainers/send_email/', views.send_email, name='send_email_table'),
]