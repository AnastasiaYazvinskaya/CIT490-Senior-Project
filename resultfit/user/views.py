from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *
from .forms import *
from client.models import ClientTrainer
from trainer.models import Qualification
from fooddairy.models import DayMenu, Recipe
from training.models import Training

from django.utils import timezone
from datetime import datetime

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
    foodPurpose = FoodDairyGeneral.objects.filter(user = request.user)[0]
    todayMenu = DayMenu.objects.filter(user = request.user, day = timezone.now().date())
    if len(todayMenu) == 0:
        todayMenu = DayMenu.objects.create(
            day = timezone.now().date(),
            user = request.user
        )
    else:
        todayMenu = todayMenu[0]
    print(datetime.now().weekday())
    training = Training.objects.filter(user = request.user, weekDay = datetime.now().weekday())
    #recipes = todayMenu.recipes.all().order_by('mealType__id')
    return render(request, 'home.html', {'menu': todayMenu, 'foodPurpose': foodPurpose, 'training':training, 'activeHome': True})

@login_required
def profile(request):
    profile = Profile.objects.get(user = request.user)
    qualification = Qualification.objects.filter(profile = profile)#.order_by('-pk')
    hasTrainer = ClientTrainer.objects.filter(client__user=request.user)
    if (len(hasTrainer) != 0):
        hasTrainer = hasTrainer[0]
    return render(request, 'profile.html', {'hasTrainer': hasTrainer, 'profile': profile, 'qualification': qualification})

# Create/Edit profile page
@login_required
def update_profile(request):
    profileObj = Profile.objects.get(user = request.user)
    files = File.objects.filter(user = profileObj)
    if files != None and len(files) != 0:
        extra = 0
    else: extra = 1
    userObj = request.user
    if request.method == "POST":
        form1 = ProfileForm(request.POST, request.FILES, instance = profileObj)
        form2 = UserForm(request.POST, request.FILES, instance = userObj)
        fileFormset = modelformset_factory(File, form=FileForm, extra=extra, can_delete=True)
        formset = fileFormset(request.POST, request.FILES, queryset=files)
        if form1.is_valid():
            # Предсохраняем данные введенные с формы (но не вносим в базу)
            profile = form1.save(commit=False)
            user = form2.save(commit=False)
            # Переносим все изменения в базу
            profile.save()
            user.save()
            for form in formset:
                file = form.save(commit=False)
                if file.file != None:
                    file.save()
            for form in formset.deleted_forms:
                file = form.save(commit=False)
                file.delete()
            return redirect('profile')
    else:
        form1 = ProfileForm(instance = profileObj)
        form2 = UserForm(instance = userObj)
        fileFormset = modelformset_factory(File, form=FileForm, extra=extra, can_delete=True)
        formset = fileFormset(queryset=files)
        print(formset)
    return render(request, "profile_update.html", {'form1': form1, 'form2': form2, 'formset': formset})
