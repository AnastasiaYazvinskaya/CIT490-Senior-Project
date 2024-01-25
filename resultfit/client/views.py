from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *
from user.models import Profile
   
# Clients page
@login_required
def clients(request):#Список клиентов для тренера
    if request.user.groups.filter(name='trainer').exists():
        clients = ClientTrainer.objects.all().order_by('id', 'active')
        
        # Получение значения из поля поиска
        search = request.GET.get('search')
        if search:
            # Фильтрация списка
            clients = clients.filter(client_firstName__icontains = search)|clients.filter(client_lastName__icontains = search)|clients.filter(client_email__icontains = search)
        return render(request, 'clients.html', {'clients': clients, 'search': search, 'activeClient': True})
    return redirect('home')

# Client page
@login_required
def client(request, pk=None):
    if request.user.groups.filter(name='trainer').exists():
        if pk:
            client = Profile.objects.get(pk=pk)
            return render(request, 'client_profile.html', {'client': client, 'activeClient': True})
        return redirect('clients')
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