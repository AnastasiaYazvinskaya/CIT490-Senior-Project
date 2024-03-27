from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.core.validators import RegexValidator

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ('name', 'time', 'weekDay') 


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = TrainingExercise
        fields = ('exercise', 'repeatNum', 'timesNum')
        


