from django import forms 
from .models import *

class ActivityTypeForm(forms.ModelForm):
    class Meta:
        model = ActivityType
        fields = ('name', 'rate', 'description') 

    '''def clean(self):
        cleaned_data = super().clean()
        if ActivityType.objects.filter(name=cleaned_data.get('name')).exists():
            self.add_error('name', "Активность с таким именем уже существует")
    '''

class PurposeTypeForm(forms.ModelForm):
    class Meta:
        model = PurposeType
        fields = ('name', 
                'proteins_rate_min', 'proteins_rate_max',
                'fats_rate_min', 'fats_rate_max',
                'carbohydrates_rate_min', 'carbohydrates_rate_max') 

    '''def clean(self):
        cleaned_data = super().clean()
        if PurposeType.objects.filter(name=cleaned_data.get('name')).exists():
            self.add_error('name', "Цель с таким именем уже существует")
    '''

class PrivacyTypeForm(forms.ModelForm):
    class Meta:
        model = PrivacyType
        fields = ('name', 'description') 

    '''def clean(self):
        cleaned_data = super().clean()
        print('id', cleaned_data.get('id'))
        if PrivacyType.objects.filter(name=cleaned_data.get('name')).exists():
            self.add_error('name', "Тип приватности с таким именем уже существует")
    '''
    
class UnitTypeForm(forms.ModelForm):
    class Meta:
        model = UnitType
        fields = ('name', 
                'full_name', 'description') 

    '''def clean(self):
        cleaned_data = super().clean()
        if PurposeType.objects.filter(name=cleaned_data.get('name')).exists():
            self.add_error('name', "Цель с таким именем уже существует")
    '''
