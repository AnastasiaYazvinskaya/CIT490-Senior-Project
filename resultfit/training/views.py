from datetime import datetime, timedelta, timezone
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *
from .forms import *
from client.models import ClientTrainer

@login_required
def sport(request, day=None):
    print(datetime.now().weekday())
    trainNote = list(TrainingNote.objects.filter(user = request.user).order_by('-day').values('day'))
    print(trainNote)
    if len(trainNote) == 0:
        trainNote = [{'day': timezone.now().date()}]
    elif trainNote[0]['day'] != timezone.now().date():
        trainNote.insert(0,{'day': timezone.now().date()})
    if day is None:
        day = timezone.now().date()
    else:
        day = datetime.strptime(day, '%Y-%m-%d').date()
        if day > timezone.now().date():
            trainNote.insert(0,{'day': day})
    training = Training.objects.filter(user = request.user, weekDay = day.weekday()).values()
    for i in training:
        i['exercises'] = TrainingExercise.objects.filter(training = i['id'])
    hasTrainer = ClientTrainer.objects.filter(client__user=request.user)
    if (len(hasTrainer) == 0):
        trainers = Profile.objects.filter(user__groups__name='trainer').exclude(user = request.user).order_by('-trainer_rating')[0:3]
    else:
        hasTrainer = hasTrainer[0]
        trainers = None

    return render(request, 'sport.html', {'trainers': trainers, 'hasTrainer': hasTrainer, 'days':trainNote,'training': training,'activeSport': True, "activeDay": day, 'newDay':trainNote[0]['day']+timedelta(days=1), 'today':timezone.now().date()})

@login_required
def sport_plan(request):
    plan = Training.objects.filter(user = request.user).order_by('weekDay')
    hasTrainer = ClientTrainer.objects.filter(client__user=request.user)
    if (len(hasTrainer) == 0):
        trainers = Profile.objects.filter(user__groups__name='trainer').exclude(user = request.user).order_by('-trainer_rating')[0:3]
    else:
        hasTrainer = hasTrainer[0]
        trainers = None
    return render(request, 'sport_plan.html', {'hasTrainer':hasTrainer, 'trainers':trainers, 'plan': plan, 'activeSport': True})

@login_required
def sport_plan_read(request, pk=None):
    if pk:
        training = Training.objects.get(pk=pk)
        exercises = TrainingExercise.objects.filter(training = training)
        return render(request, 'sport_plan_read.html', {'train': training, 'exercises': exercises, 'activeSport': True})
    return redirect('sport_plan')


@login_required
def sport_plan_create_update(request, week=None, pk=None, client=None):
    if pk != None:
        # Если ключ передан, то ищем объект
        trainingObj = Training.objects.get(pk = pk)
        exercises = TrainingExercise.objects.filter(training = trainingObj)
    else: 
        # Если ключ не передан, то работаем с пустым объектом
        trainingObj = Training()
        trainingObj.weekDay = week
        exercises = TrainingExercise.objects.none()
    if exercises != None and len(exercises) != 0:
        extra = 0
    else: extra = 1
    print('client.pk', client)
    if client:
        client = Profile.objects.get(pk=client)
        trainingObj.name = 'Тренировка с тренером'
    print('client', client)
    if request.method == "POST":
        print('method POST')
        trainingForm = TrainingForm(request.POST, request.FILES, instance = trainingObj)
        TrainingExerciseFormset = modelformset_factory(TrainingExercise, form=ExerciseForm, extra=extra, can_delete=True)
        formset = TrainingExerciseFormset(request.POST, queryset=exercises)
        print(formset.errors)
        print(trainingForm.is_valid())
        if trainingForm.is_valid() and formset.is_valid():
            print('forms valid')
            # Предсохраняем данные введенные с формы (но не вносим в базу)
            training = trainingForm.save(commit=False)
            if training.user is None:
                if client:
                    training.user = client.user
                else:
                    training.user = request.user
            # Переносим все изменения в базу
            training.save()
            print('training saved')
            for form in formset:
                print('TrainingExercise saved')
                exercise = form.save(commit=False)
                if exercise.training is None:
                    exercise.training = training
                exercise.save()
    
            for form in formset.deleted_forms:
                exercise = form.save(commit=False)
                exercise.delete()
                pass
            #form.save_m2m()
            print('INGREDINETS saved')
            training.save()
            print('training kpfc updates')
            if client:
                return redirect('client_sport', client.pk)
            return redirect('sport_plan')
    else:
        trainingForm = TrainingForm(instance = trainingObj)
        TrainingExerciseFormset = modelformset_factory(TrainingExercise, form=ExerciseForm, extra=extra, can_delete=True)
        formset = TrainingExerciseFormset(queryset=exercises)
    return render(request, "sport_plan_create_update.html", {'form': trainingForm, 'formset': formset, 'pk': pk, 'client': client, 'activeSport': True})

@login_required
def choose_trainer(request):
    print('choose_trainer')
    trainer_pk = request.GET.get('trainer', None)
    print(trainer_pk)
    trainer = User.objects.get(pk=trainer_pk)
    client = Profile.objects.get(user = request.user)
    is_exist = len(ClientTrainer.objects.filter(client=client, trainer=trainer)) > 0
    if not is_exist:
        ClientTrainer.objects.create(
            client=client,
            trainer=trainer
        )
        response = {
            'trainer': f'{trainer.last_name} {trainer.first_name}'
        }
    else:
        response = {
            'error': 'Вы уже отправляли заявку этому тренеру.'
        }
    print('responce', response)
    return JsonResponse(response)

