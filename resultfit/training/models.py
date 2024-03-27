from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from user.models import Profile
from systemdata.models import Exercise
    
class Training(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name ='Название', default=None)
    weekDay = models.IntegerField(blank=True, null=True, default=None)
    
    def __str__(self):
        return self.name

class TrainingExercise(models.Model):
    training = models.ForeignKey(Training, on_delete=models.PROTECT, null=True, blank=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT, null=True, blank=True)
    repeatNum = models.IntegerField(blank=True, null=True, default=None)
    timesNum = models.IntegerField(blank=True, null=True, default=None)

class TrainingNote(models.Model):
    day = models.DateField(verbose_name ='День', blank=True, null=True, default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    training = models.ForeignKey(Training, on_delete=models.PROTECT, null=True, blank=True)