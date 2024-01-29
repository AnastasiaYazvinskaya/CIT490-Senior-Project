from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

@login_required
def recipes(request):
    #active = bool(request.GET.get('active'))
    #activities = ActivityType.objects.filter(active = active).order_by('id')
        
    # Получение значения из поля поиска
    #search = request.GET.get('search')
    #if search:
        # Фильтрация списка
        #activities = activities.filter(name__icontains = search)
        
    #return render(request, 'activity/activities.html', {'activities': activities, 'search': search, 'active': active, 'activeActivity': True})
    return render(request, 'recipes.html', {'activeRecipe': True})