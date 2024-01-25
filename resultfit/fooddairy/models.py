from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

class FoodDairyGeneral(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    kkal = models.IntegerField(verbose_name ='Ккалории', blank=True, null=True, default=None)
    proteins = models.IntegerField(verbose_name ='Белки', blank=True, null=True, default=None)
    fats = models.IntegerField(verbose_name ='Жиры', blank=True, null=True, default=None)
    carbohydrates = models.IntegerField(verbose_name ='Углеводы', blank=True, null=True, default=None)
    
    def __str__(self):
        return f'{self.kkal}/{self.proteins}/{self.fats}/{self.carbohydrates}'

# triggred when User object is created
@receiver(post_save, sender=FoodDairyGeneral)
def user_created(sender, instance, created, **kwargs):
    if created:
        pass

