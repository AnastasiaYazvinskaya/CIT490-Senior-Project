from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from training.models import Training, TrainingExercise
from .models import *
from user.models import Profile
from fooddairy.models import *
from recipe.models import *
   
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
def client_meal(request, pk=None, day=None):
    if request.user.groups.filter(name='trainer').exists():
        if pk:
            client = Profile.objects.get(pk=pk)
            dayNotes = DayMenu.objects.filter(user = client.user).order_by('-day')
            dairy = FoodDairyGeneral.objects.get(user = client.user)
            print('day', day)
            if day is None:
                day = timezone.now().date()
            else:
                day = datetime.strptime(day, '%Y-%m-%d')
            print('day2', day)
            todayMenu = DayMenu.objects.filter(user = client.user, day = day)
            print('todayMenu', todayMenu)
            if len(todayMenu) == 0:
                todayMenu = DayMenu.objects.create(
                    day = timezone.now().date(),
                    user = client.user
                )
            else:
                todayMenu = todayMenu[0]
            day = todayMenu.day
            note = FoodDairyNote.objects.filter(day__day=day)
            breakfastNote=None
            breakfastIngred=None
            lanchNote=None
            lanchIngred=None
            dinnerNote=None
            dinnerIngred=None
            snackNote=None
            snackIngred=None
            if len(note) != 0:
                breakfastNote = note.values()[0]
                breakfastIngred = Ingredient.objects.filter(recipe=todayMenu.braekfast.recipes)
                if len(breakfastNote) != 0:
                    breakfastNote['comments'] = Comment.objects.filter(foodNote=note[0]).order_by('-created_by')
                lanchNote = note.values()[0]
                lanchIngred = Ingredient.objects.filter(recipe=todayMenu.lanch.recipes)
                if len(lanchNote) != 0:
                    lanchNote['comments'] = Comment.objects.filter(foodNote=note[0]).order_by('-created_by')
                dinnerNote = note.values()[0]
                dinnerIngred = Ingredient.objects.filter(recipe=todayMenu.dinner.recipes)
                if len(dinnerNote) != 0:
                    dinnerNote['comments'] = Comment.objects.filter(foodNote=note[0]).order_by('-created_by')
                if todayMenu.snack:
                    snackNote = note.values()[0]
                    snackIngred = Ingredient.objects.filter(recipe=todayMenu.snack.recipes)
                    if len(snackNote) != 0:
                        snackNote['comments'] = Comment.objects.filter(foodNote=note[0]).order_by('-created_by')
                
            return render(request, 'client_meal.html', {"days": dayNotes, "dairy": dairy, 'menu': todayMenu, "activeDay": day, 'client': client,
                                                        'breakfastNote': breakfastNote, 'breakfastIngred':breakfastIngred, 
                                                        'lanchNote': lanchNote, 'lanchIngred':lanchIngred, 
                                                        'dinnerNote': dinnerNote, 'dinnerIngred':dinnerIngred, 
                                                        'snackNote': snackNote, 'snackIngred':snackIngred,
                                                        'activeClient': True, 'activeClientMeal': True})
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

