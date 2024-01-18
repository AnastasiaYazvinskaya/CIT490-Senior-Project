from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
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
                return redirect('profile')
            else:
                return render(request, 'register.html', {'form': form})
        form = RegisterForm
        return render(request, 'register.html', {'form': form})
    
def trainer_register(request, code=None):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = TrainerRegisterForm(request.POST)
            code = request.POST['code']
            trainer = PrepareUser.objects.get(code=code)
            if (trainer and not trainer.user):
                if form.is_valid():
                    user = form.save(commit=False)
                    user.save()
                    group = Group.objects.get(name='trainer')
                    group.user_set.add(user)
                    trainer.user = user
                    trainer.save()
                    login(request, user)
                    #request.session['username'] = user.username
                    return redirect('profile')
                else:
                    return render(request, 'trainer/trainer_register.html', {'form': form, 'code': code})
            else:
                messages.error(request, 'Тренер по этому коду уже зарегистрирован')
                return render(request, 'trainer/trainer_register.html', {'form': form, 'code': code})
        if code:
            if PrepareUser.objects.filter(code=code).exists():
                trainer = PrepareUser.objects.get(code=code)
            else:
                messages.error(request, f'Приглашений с кодом {code} не обнаружено')
                return redirect('register')
            form = TrainerRegisterForm(instance = User(last_name = trainer.lastName, first_name = trainer.firstName, email = trainer.email))
        else:
            form = TrainerRegisterForm
        return render(request, 'trainer/trainer_register.html', {'form': form, 'code': code})

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

# Trainers page
@login_required
def trainers(request):
    if request.user.groups.filter(name='administrator').exists():
        trainers = PrepareUser.objects.all().order_by('active')
        
        # Получение значения из поля поиска
        search = request.GET.get('searchTrainer')
        if search:
            # Фильтрация списка
            trainers = trainers.filter(firstName__icontains = search)|trainers.filter(lastName__icontains = search)|trainers.filter(email__icontains = search)
        return render(request, 'trainer/trainers.html', {'trainers': trainers, 'search': search})
    return redirect('home')

# Trainer page
@login_required
def trainer(request, pk=None):
    if request.user.groups.filter(name='administrator').exists():
        if id:
            trainer = PrepareUser.objects.get(pk=pk)
            return render(request, 'trainer/trainer_read.html', {'trainer': trainer})
        return redirect('trainers')
    return redirect('home')

from django.core import mail
from django.core.mail.backends.smtp import EmailBackend
# Create/Edit trainer page
@login_required
def create_update_trainer(request, pk=None):
    connection = mail.get_connection()
    print('connection', connection)
    if pk != None:
        # Если ключ передан, то ищем объект
        trainerObj = PrepareUser.objects.get(pk = pk)
    else: 
        # Если ключ не передан, то работаем с пустым объектом
        trainerObj = None
    if request.method == "POST":
        form = PrepareUserForm(request.POST, request.FILES, instance = trainerObj)
        if form.is_valid():
            # Предсохраняем данные введенные с формы (но не вносим в базу)
            trainer = form.save(commit=False)
            # Переносим все изменения в базу
            trainer.save()
            #form.save_m2m()
            return redirect('trainers')
    else:
        form = PrepareUserForm(instance = trainerObj)
    return render(request, "trainer/trainer_create_update.html", {'form': form, 'pk': pk})

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
        
def validate_code(request):
    code = request.GET.get('code', None)
    print('code', code)
    trainer = PrepareUser.objects.filter(code=code).values().first()
    if (code != None):
        response = {
            'trainer': trainer
        }
    else:
        response = {
            'error': 'Введите код'
        }
        print('response', response)
    return JsonResponse(response)

def send_email(request):
    email = request.GET.get('email', None)
    response = {
        'email': email
    }
    if email:
        trainer = PrepareUser.objects.filter(email=email).values().first()
        html_message = render_to_string("email/trainerCode.html", {'trainer': trainer})
        plain_message = strip_tags(html_message)

        message = EmailMultiAlternatives(
            subject = 'Создание тренерского аккаунта', 
            body = plain_message,
            from_email = settings.EMAIL_HOST_USER,
            to= [email]
        )

        message.attach_alternative(html_message, "text/html")
        message.send()
    else:
        response.error = 'Пустая почта'
    return JsonResponse(response)
