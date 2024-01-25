from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *
from user.models import Group
from .forms import *

@login_required
def systemdata(request):
    if request.user.groups.filter(name='programmer').exists():
        return redirect('activity')
    return redirect('home')

@login_required
def activity(request):
    if request.user.groups.filter(name='programmer').exists():
        activities = ActivityType.objects.all().order_by('id')
        
        # Получение значения из поля поиска
        search = request.GET.get('search')
        if search:
            # Фильтрация списка
            activities = activities.filter(name__icontains = search)
        return render(request, 'activity/activities.html', {'activities': activities, 'search': search, 'activeActivity': True})
    return redirect('home')

@login_required
def purpose(request):
    if request.user.groups.filter(name='programmer').exists():
        purposes = PurposeType.objects.all().order_by('id')
        
        # Получение значения из поля поиска
        search = request.GET.get('search')
        if search:
            # Фильтрация списка
            purposes = purposes.filter(name__icontains = search)
        return render(request, 'purpose/purposes.html', {'purposes': purposes, 'search': search, 'activePurpose': True})
    return redirect('home')

# Create/Edit activity page
@login_required
def create_update_activity(request, pk=None):
    if pk != None:
        # Если ключ передан, то ищем объект
        activityObj = ActivityType.objects.get(pk = pk)
    else: 
        # Если ключ не передан, то работаем с пустым объектом
        activityObj = None
    if request.method == "POST":
        form = ActivityTypeForm(request.POST, request.FILES, instance = activityObj)
        if form.is_valid():
            # Предсохраняем данные введенные с формы (но не вносим в базу)
            activity = form.save(commit=False)
            # Переносим все изменения в базу
            activity.save()
            #form.save_m2m()
            return redirect('activity')
    else:
        form = ActivityTypeForm(instance = activityObj)
    return render(request, "activity/activity_create_update.html", {'form': form, 'pk': pk, 'activeActivity': True})

# Create/Edit purpose page
@login_required
def create_update_purpose(request, pk=None):
    if pk != None:
        # Если ключ передан, то ищем объект
        purposeObj = PurposeType.objects.get(pk = pk)
    else: 
        # Если ключ не передан, то работаем с пустым объектом
        purposeObj = None
    if request.method == "POST":
        form = PurposeTypeForm(request.POST, request.FILES, instance = purposeObj)
        if form.is_valid():
            # Предсохраняем данные введенные с формы (но не вносим в базу)
            purpose = form.save(commit=False)
            # Переносим все изменения в базу
            purpose.save()
            #form.save_m2m()
            return redirect('purpose')
    else:
        form = PurposeTypeForm(instance = purposeObj)
    return render(request, "purpose/purpose_create_update.html", {'form': form, 'pk': pk, 'activePurpose': True})

# Delete activity 
@login_required
def delete_activity(request, pk=None):
    activityObj = ActivityType.objects.get(pk = pk)
    activityObj.delete()
    return redirect('activity')

# Delete purpose 
@login_required
def delete_purpose(request, pk=None):
    purposeObj = PurposeType.objects.get(pk = pk)
    purposeObj.delete()
    return redirect('purpose')
    

