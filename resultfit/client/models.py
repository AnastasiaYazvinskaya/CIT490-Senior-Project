from django.db import models
from django.contrib.auth.models import User
    
class ClientTrainer(models.Model):
    client = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='Клиент')
    trainer = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='Тренер')
    active = models.BooleanField(default=True, verbose_name ='Активность', blank=True)
