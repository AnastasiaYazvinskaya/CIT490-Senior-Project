from django.db import models
from django.contrib.auth.models import User
from user.models import Profile
    
class ClientTrainer(models.Model):
    client = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True, blank=True, related_name='Клиент')
    trainer = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='Тренер')
    active = models.BooleanField(default=False, verbose_name ='Активность', blank=True)
