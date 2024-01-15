from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                messages.success(request, 'You have singed up successfully.')
                login(request, user)
                #request.session['username'] = user.username
                return redirect('profile')
            else:
                return render(request, 'register.html', {'form': form})
        form = RegisterForm
        return render(request, 'register.html', {'form': form})
    

def login_user(request):
    if request.session.has_key('username'):#request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user:
                    messages.success(request, 'You have singed up successfully.')
                    login(request, user)
                    #request.session['username'] = user.username
                    return redirect('home')
            else:
                messages.error(request,f'Invalid username or password')
                return render(request, 'login.html', {'form': form})
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def reset_password(request):
    return render(request, 'password/reset.html')

@login_required
def logout_user(request):
    logout(request)
    #del request.session['username']
    return redirect('start_page')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def home(request):
    return render(request, 'home.html')