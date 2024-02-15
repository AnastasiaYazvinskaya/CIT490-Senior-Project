from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from fooddairy.models import FoodDairyGeneral
from systemdata.models import ActivityType, PurposeType

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    phone = models.CharField(max_length=12, verbose_name="Телефон", blank=True, null=True, default=None)
    height = models.CharField(max_length=20, verbose_name ='Рост', blank=True, null=True, default=None)
    weight = models.CharField(max_length=20, verbose_name ='Вес', blank=True, null=True, default=None)
    activity = models.ForeignKey(ActivityType, on_delete=models.PROTECT, verbose_name ='Активность', blank=True, null=True, default=None)
    age = models.IntegerField(verbose_name ='Возраст', blank=True, null=True, default=None)
    trainer_rating = models.FloatField(default=0, blank=True, null=True)
    SEX_CHOICES = (
        ('F', 'Женщина',),
        ('M', 'Мужчина',),
    )
    sex = models.CharField(max_length=1, blank=True, null=True, default=None)
    purpose = models.ForeignKey(PurposeType, on_delete=models.PROTECT, verbose_name ='Цель', blank=True, null=True, default=2)
    
    def __str__(self):
        return self.user.username

class File(models.Model):
    file = models.FileField(upload_to='user/assets/media', verbose_name='file')
    user = models.ForeignKey(Profile, on_delete=models.PROTECT, verbose_name ='Активность', blank=True, null=True, default=None)


# triggred when User object is created
@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='base')
        group.user_set.add(instance)
        Profile.objects.create(
            user=instance
        )
        FoodDairyGeneral.objects.create(
            user=instance
        )

