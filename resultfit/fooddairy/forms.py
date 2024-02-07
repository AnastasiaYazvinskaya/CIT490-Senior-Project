from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.core.validators import RegexValidator

class FoodDairyNoteForm(forms.ModelForm):
    class Meta:
        model = FoodDairyNote
        fields = ('image', 'kkal', 'proteins', 'fats', 'carbohydrates') 


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        