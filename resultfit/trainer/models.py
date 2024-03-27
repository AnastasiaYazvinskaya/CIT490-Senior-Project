from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from user.models import Profile
from systemdata.models import FileType
    
class PrepareUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    firstName = models.CharField(max_length=20, verbose_name ='Имя', default=None)
    lastName = models.CharField(max_length=20, verbose_name ='Фамилия', default=None)
    email = models.CharField(max_length=30, verbose_name ='E-mail', default=None)
    code = models.CharField(max_length=20, verbose_name ='Код регистрации', default=None)
    active = models.BooleanField(default=True, verbose_name ='Активность', blank=True)
    
    def __str__(self):
        return (self.firstName + self.lastName)
    
class Qualification(models.Model):
    file = models.FileField(upload_to='trainer/assets/media', verbose_name='file', null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, verbose_name ='Профиль', blank=True, null=True, default=None)
    type = models.ForeignKey(FileType, on_delete=models.PROTECT, verbose_name ='Тип', blank=True, null=True, default=None)

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