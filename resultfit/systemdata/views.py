from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *
from user.models import Group
from .forms import *
from recipe.models import Ingredient, Recipe

@login_required
def systemdata(request):
    if request.user.groups.filter(name='programmer').exists():
        return redirect(reverse('activity')+ '?active=True')
    return redirect('home')

@login_required
def activity(request):
    if request.user.groups.filter(name='programmer').exists():
        active = bool(request.GET.get('active'))
        activities = ActivityType.objects.filter(active = active).order_by('id')
        
        # Получение значения из поля поиска
        search = request.GET.get('search')
        if search:
            # Фильтрация списка
            activities = activities.filter(name__icontains = search)
        
        return render(request, 'activity/activities.html', {'activities': activities, 'search': search, 'active': active, 'activeActivity': True})
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
            return redirect(reverse('activity')+ '?active=True')
    else:
        form = ActivityTypeForm(instance = activityObj)
    return render(request, "activity/activity_create_update.html", {'form': form, 'pk': pk, 'activeActivity': True})

# Delete activity 
@login_required
def delete_activity(request, pk=None):
    activityObj = ActivityType.objects.get(pk = pk)
    activityObj.active = False
    activityObj.save()
    return redirect(reverse('activity')+ '?active=True')

# Activate activity 
@login_required   
def activate_activity(request, pk=None):
    activityObj = ActivityType.objects.get(pk = pk)
    activityObj.active = True
    activityObj.save()
    to_active = len(ActivityType.objects.filter(active = False)) == 0
    return redirect(reverse('activity')+ '?active='+str(to_active))

@login_required
def purpose(request):
    if request.user.groups.filter(name='programmer').exists():
        active = bool(request.GET.get('active'))
        purposes = PurposeType.objects.filter(active = active).order_by('id')
        
        # Получение значения из поля поиска
        search = request.GET.get('search')
        if search:
            # Фильтрация списка
            purposes = purposes.filter(name__icontains = search)
        return render(request, 'purpose/purposes.html', {'purposes': purposes, 'search': search, 'active': active, 'activePurpose': True})
    return redirect('home')

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
            return redirect(reverse('purpose')+ '?active=True')
    else:
        form = PurposeTypeForm(instance = purposeObj)
    return render(request, "purpose/purpose_create_update.html", {'form': form, 'pk': pk, 'activePurpose': True})

# Delete purpose 
@login_required
def delete_purpose(request, pk=None):
    purposeObj = PurposeType.objects.get(pk = pk)
    purposeObj.active = False
    purposeObj.save()
    return redirect(reverse('purpose')+ '?active=True')

# Activate purpose 
@login_required
def activate_purpose(request, pk=None):
    purposeObj = PurposeType.objects.get(pk = pk)
    purposeObj.active = True
    purposeObj.save()
    to_active = len(PurposeType.objects.filter(active = False)) == 0
    return redirect(reverse('purpose')+ '?active='+str(to_active))

@login_required
def privacy(request):
    if request.user.groups.filter(name='programmer').exists():
        active = bool(request.GET.get('active'))
        privacies = PrivacyType.objects.filter(active = active).order_by('id')
        
        # Получение значения из поля поиска
        search = request.GET.get('search')
        if search:
            # Фильтрация списка
            privacies = privacies.filter(name__icontains = search)
        return render(request, 'privacy/privacies.html', {'privacies': privacies, 'search': search, 'active': active, 'activePrivacy': True})
    return redirect('home')

# Create/Edit privacy page
@login_required
def create_update_privacy(request, pk=None):
    print('1')
    if pk != None:
        print('2')
        # Если ключ передан, то ищем объект
        privacyObj = PrivacyType.objects.get(pk = pk)
    else: 
        # Если ключ не передан, то работаем с пустым объектом
        privacyObj = None
    if request.method == "POST":
        print('3')
        form = PrivacyTypeForm(request.POST, request.FILES, instance = privacyObj)
        print(form.is_valid())
        if form.is_valid():
            print('4')
            # Предсохраняем данные введенные с формы (но не вносим в базу)
            privacy = form.save(commit=False)
            # Переносим все изменения в базу
            privacy.save()
            #form.save_m2m()
            print('redirect')
            return redirect(reverse('privacy')+ '?active=True')
    else:
        form = PrivacyTypeForm(instance = privacyObj)
    return render(request, "privacy/privacy_create_update.html", {'form': form, 'pk': pk, 'activePrivacy': True})

# Delete privacy 
@login_required
def delete_privacy(request, pk=None):
    privacyObj = PrivacyType.objects.get(pk = pk)
    privacyObj.active = False
    privacyObj.save()
    return redirect(reverse('privacy')+ '?active=True')

# Activate privacy 
@login_required
def activate_privacy(request, pk=None):
    privacyObj = PrivacyType.objects.get(pk = pk)
    privacyObj.active = True
    privacyObj.save()
    to_active = len(PrivacyType.objects.filter(active = False)) == 0
    return redirect(reverse('privacy')+ '?active='+str(to_active))

@login_required
def unit(request):
    if request.user.groups.filter(name='programmer').exists():
        active = bool(request.GET.get('active'))
        units = UnitType.objects.filter(active = active).order_by('id')
        
        # Получение значения из поля поиска
        search = request.GET.get('search')
        if search:
            # Фильтрация списка
            units = units.filter(name__icontains = search)
        return render(request, 'unit/units.html', {'units': units, 'search': search, 'active': active, 'activeUnit': True})
    return redirect('home')

# Create/Edit purpose page
@login_required
def create_update_unit(request, pk=None):
    if pk != None:
        # Если ключ передан, то ищем объект
        unitObj = UnitType.objects.get(pk = pk)
    else: 
        # Если ключ не передан, то работаем с пустым объектом
        unitObj = None
    if request.method == "POST":
        form = UnitTypeForm(request.POST, request.FILES, instance = unitObj)
        if form.is_valid():
            # Предсохраняем данные введенные с формы (но не вносим в базу)
            unit = form.save(commit=False)
            # Переносим все изменения в базу
            unit.save()
            #form.save_m2m()
            return redirect(reverse('unit')+ '?active=True')
    else:
        form = UnitTypeForm(instance = unitObj)
    return render(request, "unit/unit_create_update.html", {'form': form, 'pk': pk, 'activeUnit': True})

# Delete unit 
@login_required
def delete_unit(request, pk=None):
    unitObj = UnitType.objects.get(pk = pk)
    unitObj.active = False
    unitObj.save()
    return redirect(reverse('unit')+ '?active=True')

# Activate unit 
@login_required
def activate_unit(request, pk=None):
    unitObj = UnitType.objects.get(pk = pk)
    unitObj.active = True
    unitObj.save()
    to_active = len(UnitType.objects.filter(active = False)) == 0
    return redirect(reverse('unit')+ '?active='+str(to_active))

@login_required
def product(request):
    if request.user.groups.filter(name='programmer').exists():
        active = bool(request.GET.get('active'))
        products = Product.objects.filter(active = active).order_by('id')
        
        # Получение значения из поля поиска
        search = request.GET.get('search')
        if search:
            # Фильтрация списка
            products = products.filter(name__icontains = search)
        return render(request, 'product/products.html', {'products': products, 'search': search, 'active': active, 'activeProduct': True})
    return redirect('home')

# Create/Edit purpose page
@login_required
def create_update_product(request, pk=None):
    if pk != None:
        # Если ключ передан, то ищем объект
        productObj = Product.objects.get(pk = pk)
    else: 
        # Если ключ не передан, то работаем с пустым объектом
        productObj = None
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance = productObj)
        if form.is_valid():
            # Предсохраняем данные введенные с формы (но не вносим в базу)
            product = form.save(commit=False)
            # Переносим все изменения в базу
            product.save()
            #form.save_m2m()
            return redirect(reverse('product')+ '?active=True')
    else:
        form = ProductForm(instance = productObj)
    return render(request, "product/product_create_update.html", {'form': form, 'pk': pk, 'activeProduct': True})

# Delete product 
@login_required
def delete_product(request, pk=None):
    productObj = Product.objects.get(pk = pk)
    productObj.active = False
    productObj.save()
    return redirect(reverse('product')+ '?active=True')

# Activate product 
@login_required
def activate_product(request, pk=None):
    productObj = Product.objects.get(pk = pk)
    productObj.active = True
    productObj.save()
    to_active = len(Product.objects.filter(active = False)) == 0
    return redirect(reverse('product')+ '?active='+str(to_active))

from django.db import connection
@login_required
def reset(request):
    if request.user.groups.filter(name='programmer').exists():
        messages = []
        if request.method == "POST":
            form = request.POST
            #check database
            if form['database'].lower() == 'ingredient':
                model = Ingredient
                messages.append('Вы работали с Ингредиентами. Был выполнен скрипт:')
            if form['database'].lower() == 'recipe':
                model = Recipe
                messages.append('Вы работали с Рецептами. Был выполнен скрипт:')
            if form['database'].lower() == 'product':
                model = Product
                messages.append('Вы работали с Продуктами. Был выполнен скрипт:')
            #check filter
            if 'sql' in form.keys():
                with connection.cursor() as cursor:
                    cursor.execute(form['sql'])
                messages.append(form['sql'])
            else:
                print('not sql')
        
        model = Ingredient
        table_data = {
            'table_name': "Ingredient",
            'db_table': model._meta.db_table,
            'fields': []
        }
        for field in model._meta.get_fields():
            table_data['fields'].append({'name': field.name, 'type': field.get_internal_type()})
        return render(request, 'reset.html', {'messages': messages, 'table_data': table_data, 'activeReset': True})
    return redirect('home')

def update_table(request):
    database = request.GET.get('database', None)
    if database.lower() == 'ingredient':
        model = Ingredient
    elif database.lower() == 'recipe':
        model = Recipe
    elif database.lower() == 'product':
        model = Product
    elif database.lower() == 'mealtype':
        model = MealType
    table_data = {
        'table': {
            'table_name': database,
            'db_table': model._meta.db_table,
            'fields': []
        }
    }
    for field in model._meta.get_fields(include_parents=False):
        table_data['table']['fields'].append({'name': field.name, 'type': field.get_internal_type()})
    print(table_data)
    return JsonResponse(table_data)
