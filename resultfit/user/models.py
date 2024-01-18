from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    height = models.CharField(max_length=20, verbose_name ='Рост')
    weight = models.CharField(max_length=20, verbose_name ='Вес')
    activity = models.CharField(max_length=20, verbose_name ='Активность')
    
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

@receiver(post_save, sender=PrepareUser)
def user_created(sender, instance, created, **kwargs):
    if created:
        html_message = render_to_string("email/trainerCode.html", {'trainer': instance})
        plain_message = strip_tags(html_message)

        message = EmailMultiAlternatives(
            subject = 'Создание тренерского аккаунта', 
            body = plain_message,
            from_email = settings.EMAIL_HOST_USER,
            to= [instance.email]
        )

        message.attach_alternative(html_message, "text/html")
        message.send()
