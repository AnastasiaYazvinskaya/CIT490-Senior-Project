from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from user.models import Profile
from django.http import JsonResponse

@login_required
def fooddairy(request):
    dairy = FoodDairyGeneral.objects.get(user = request.user)
    return render(request, 'food_dairy.html', {"dairy": dairy, "activeFood": True})

@login_required
def calculate_cpfc(request, pk):
    if request.user.pk == pk:
        dairy = FoodDairyGeneral.objects.get(user = request.user)
        print('dairy', dairy)
        if (dairy != None):
            profile = Profile.objects.get(user = request.user)
            if profile.sex == 'F':
                dairy.kkal = round((655.1 + (9.563*float(profile.weight)) + (1.85*float(profile.height)) - (4.676*float(profile.age))) * float(profile.activity.rate))
            elif profile.sex == 'M':
                dairy.kkal = round((66.5 + (13.75*float(profile.weight)) + (5.003*float(profile.height)) - (6.775*float(profile.age))) * float(profile.activity.rate))
            dairy.save()
            return redirect('fooddairy')
        return redirect('profile')
    else:
        return redirect('profile')
    
@login_required
def food_dairy(request):
    return render(request, 'food_dairy/dairy.html', {"activeFood": True})
