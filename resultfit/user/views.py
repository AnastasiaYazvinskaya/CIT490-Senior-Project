from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                login(request, user)
                #request.session['username'] = user.username
                #return redirect('update_profile', Profile.objects.get(user = user).pk)
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
def home(request):
    return render(request, 'home.html', {'activeHome': True})

@login_required
def profile(request):
    profile = Profile.objects.get(user = request.user)
    return render(request, 'profile.html', {'profile': profile})

# Create/Edit profile page
@login_required
def update_profile(request, pk=None):
    if pk != None:
        # Если ключ передан, то ищем объект
        profileObj = Profile.objects.get(pk = pk)
    else: 
        # Если ключ не передан, то работаем с пустым объектом
        profileObj = None
    userObj = request.user
    if request.method == "POST":
        form1 = ProfileForm(request.POST, request.FILES, instance = profileObj)
        form2 = UserForm(request.POST, request.FILES, instance = userObj)
        if form1.is_valid():
            # Предсохраняем данные введенные с формы (но не вносим в базу)
            profile = form1.save(commit=False)
            user = form2.save(commit=False)
            # Переносим все изменения в базу
            profile.save()
            user.save()
            return redirect('profile')
    else:
        form1 = ProfileForm(instance = profileObj)
        form2 = UserForm(instance = userObj)
    return render(request, "profile_update.html", {'form1': form1, 'form2': form2, 'pk': pk})
