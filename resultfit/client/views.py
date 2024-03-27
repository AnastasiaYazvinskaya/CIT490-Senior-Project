from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from training.models import Training, TrainingExercise
from .models import *
from user.models import Profile
from fooddairy.models import FoodDairyGeneral
   
# Clients page
@login_required
def clients(request, type):#Список клиентов для тренера
    if request.user.groups.filter(name='trainer').exists():
        if type == 'current':
            clients = ClientTrainer.objects.filter(trainer = request.user, active = True).order_by('id')
        elif type == 'request':
            clients = ClientTrainer.objects.filter(trainer = request.user, active = False).order_by('id')
        requestNum = len(ClientTrainer.objects.filter(trainer = request.user, active = False))
        
        # Получение значения из поля поиска
        search = request.GET.get('search')
        if search:
            pass
            # Фильтрация списка
            #clients = clients.filter(client_firstName__icontains = search)|clients.filter(client_lastName__icontains = search)|clients.filter(client_email__icontains = search)
        return render(request, 'clients.html', {'clients': clients, 'search': search, 'activeCurrent': type == 'current', 'activeRequest': type == 'request', 'requestNum': requestNum})
    return redirect('home')

# Client page
@login_required
def client(request, pk=None):
    if request.user.groups.filter(name='trainer').exists():
        if pk:
            client = Profile.objects.get(pk=pk)
            recommends = FoodDairyGeneral.objects.get(user=client.user)
            return render(request, 'client_profile.html', {'client': client, 'recommends': recommends, 'activeClient': True, 'activeClientData': True})
        return redirect('clients')
    return redirect('home')

# Client page
@login_required
def client_meal(request, pk=None):
    if request.user.groups.filter(name='trainer').exists():
        if pk:
            client = Profile.objects.get(pk=pk)
            recommends = FoodDairyGeneral.objects.get(user=client.user)
            return render(request, 'client_meal.html', {'client': client, 'recommends': recommends, 'activeClient': True, 'activeClientMeal': True})
        return redirect('clients')
    return redirect('home')

# Client page
@login_required
def client_sport(request, pk=None):
    if request.user.groups.filter(name='trainer').exists():
        if pk:
            todayWeek = timezone.now().date().weekday()
            client = Profile.objects.get(pk=pk)
            plan = Training.objects.filter(user = client.user).order_by('weekDay')
            todayTrainings = Training.objects.filter(user = client.user, weekDay=todayWeek).values()
            for i in todayTrainings:
                i['exercises'] = TrainingExercise.objects.filter(training = i['id'])
            return render(request, 'client_sport.html', {'client': client, 'plan': plan, 'todayTrainings': todayTrainings, 'activeClient': True, 'activeClientSport': True, 'todayWeek': todayWeek})
        return redirect('clients')
    return redirect('home')

@login_required
def accept_client(request, pk):
    if request.user.groups.filter(name='trainer').exists():
        if pk:
            client = ClientTrainer.objects.get(pk=pk)
            if (client.trainer == request.user):
                client.active = True
                client.save()
        requestNum = len(ClientTrainer.objects.filter(active = False))
        if requestNum > 0:
            type = 'request'
        else:
            type = 'current'
        return redirect('clients', type)
    return redirect('home')


"""
# Deactivate trainer
@login_required
def delete_trainer(request, pk=None):
    trainer = PrepareUser.objects.get(pk = pk)
    
    if request.method == "POST":
        trainer.active = False
        template = request.POST['template']
        # Переносим все изменения в базу
        trainer.save()
        if template == 'list':
            return redirect('trainers')
        elif template == 'card':
            return redirect('trainer', pk=trainer.pk)
"""

