from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.user.username
    
class PrepareUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    firstName = models.CharField(max_length=20, verbose_name ='Имя')
    lastName = models.CharField(max_length=20, verbose_name ='Фамилия')
    email = models.CharField(max_length=30, verbose_name ='E-mail')
    code = models.CharField(max_length=20, verbose_name ='Код регистрации')
    active = models.BooleanField(default=True, verbose_name ='Активность')
    
    def __str__(self):
        return (self.firstName + self.lastName)

# triggred when User object is created
@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='base')
        group.user_set.add(instance)
        Profile.objects.create(
            user=instance
        )