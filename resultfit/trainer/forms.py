from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.core.validators import RegexValidator

class TrainerRegisterForm(UserCreationForm):
    username = forms.CharField(validators=[RegexValidator(
        '[a-zA-Z0-9]{5,}', message="Введите корректное имя пользователя. Он должен содержать английские буквы и цифры. Его длина должна быть не менее 5")], label='Имя пользователя')
    password1 = forms.CharField(label="Пароль", strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтверждение пароля", strip=False, widget=forms.PasswordInput)
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Фамилия')
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Имя')
    email = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='E-mail')
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'username', 'email', 'password1', 'password2', 'groups']

    def clean(self):
        cleaned_data = super().clean()
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            self.add_error('email', "Эта почта уже используется")
        if User.objects.filter(username=cleaned_data.get('username')).exists():
            self.add_error('username', "Это имя пользователя уже используется")

class PrepareUserForm(forms.ModelForm):
    code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Код регистрации')
    class Meta:
        model = PrepareUser
        fields = ('lastName', 'firstName', 'email', 'code') 

    def clean(self):
        cleaned_data = super().clean()
        if PrepareUser.objects.filter(email=cleaned_data.get('email')).exists():
            self.add_error('email', "Эта почта уже используется")
        if PrepareUser.objects.filter(code=cleaned_data.get('code')).exists():
            self.add_error('code', "КАжется код случайно повторился, обновите код.")


