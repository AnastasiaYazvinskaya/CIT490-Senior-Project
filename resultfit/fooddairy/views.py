from datetime import datetime
from datetime import timedelta 
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from user.models import Profile
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

@login_required
def fooddairy(request, day=None):
    dayNotes = DayMenu.objects.filter(user = request.user).order_by('-day')
    dairy = FoodDairyGeneral.objects.get(user = request.user)
    print('day', day)
    if day is None:
        day = timezone.now().date()
    else:
        day = datetime.strptime(day, '%Y-%m-%d')
    print('day2', day)
    todayMenu = DayMenu.objects.filter(user = request.user, day = day)
    print('todayMenu', todayMenu)
    if len(todayMenu) == 0:
        todayMenu = DayMenu.objects.create(
            day = timezone.now().date(),
            user = request.user
        )
    else:
        todayMenu = todayMenu[0]
    day = todayMenu.day
    return render(request, 'food_dairy.html', {"days": dayNotes, "dairy": dairy, 'menu': todayMenu, "activeFood": True, "activeDay": day, 'newDay':dayNotes[0].day+timedelta(days=1), 'curTime':int(timezone.now().strftime('%H'))})

@login_required
def calculate_cpfc(request):
    dairy = FoodDairyGeneral.objects.get(user = request.user)
    if (dairy != None):
        profile = Profile.objects.get(user = request.user)
        if profile.sex == 'F':
            dairy.kkal = round((655.1 + (9.563*float(profile.weight)) + (1.85*float(profile.height)) - (4.676*float(profile.age))) * float(profile.activity.rate))
        elif profile.sex == 'M':
            dairy.kkal = round((66.5 + (13.75*float(profile.weight)) + (5.003*float(profile.height)) - (6.775*float(profile.age))) * float(profile.activity.rate))
        dairy.proteins = round(dairy.kkal * float(profile.purpose.proteins_rate_min) / 100)
        dairy.fats = round(dairy.kkal * float(profile.purpose.fats_rate_min) / 100)
        dairy.carbohydrates = round(dairy.kkal * float(profile.purpose.carbohydrates_rate_max) / 100)
        dairy.save()
        return redirect('fooddairy')
    return redirect('profile')
    
@login_required
def food_dairy(request, day=None):
    dayNotes = DayNote.objects.filter(user = request.user).order_by('-day')
    if len(dayNotes) == 0:
        dayNotes = {}
        day = timezone.now().date()
        notes = {}
    else:
        if day is None:
            day = dayNotes[0]
        else:
            day = dayNotes.filter(day = datetime.strptime(day, '%Y-%m-%d'))[0]
        
        notesQ = day.foodday.all()#.order_by('-mealType__id')
        notes = notesQ.values()
        for idy, note in enumerate(notes):
            note['comments'] = notesQ[idy].foodnote.all().order_by('-created_by')
            if notesQ[idy].image:
                note['image_url'] = notesQ[idy].image.url
            elif notesQ[idy].recipes:
                note['recipes'] = notesQ[idy].recipes.name
            note['mealType'] = notesQ[idy].mealType.name
        day = day.day
    
    return render(request, 'food_dairy/dairy.html', {"days": dayNotes, "notes": notes, "activeFood": True, "activeDay": day})

def meal(request, pk):
    return render(request, 'food_dairy/meal.html', {"activeFood": True})

def add_note(request, meal=None):
    newNote = FoodDairyNote()
    dayNote = DayNote()
    dayNote.day = timezone.now().date()
    if meal != None:
        # Если ключ передан, то ищем объект
        meal = MealDetail.objects.get(pk = meal)
        newNote.mealType = meal.mealType
        newNote.kkal = meal.kkal
        newNote.proteins = meal.proteins
        newNote.fats = meal.fats
        newNote.carbohydrates = meal.carbohydrates
        newNote.recipes = meal.recipes
    else: 
        # Если ключ не передан, то работаем с пустым объектом
        meal = None
    if request.method == "POST":
        form1 = FoodDairyNoteForm(request.POST, request.FILES, instance = newNote)
        form2 = DayNoteForm(request.POST, request.FILES, instance = dayNote)
        if form1.is_valid() and form2.is_valid():
            # Предсохраняем данные введенные с формы (но не вносим в базу)
            note = form1.save(commit=False)
            # Переносим все изменения в базу
            day = form2.save(commit=False)
            day.user = request.user
            day.save()
            note.day = day
            note.save()
            comment = request.POST.get('comment', None)
            print(comment)
            if comment:
                comment = Comment.objects.create(
                    author = request.user,
                    created_by = timezone.now(),
                    text = comment,
                    foodNote = note
                )
            meal.is_noted = True
            meal.save()
            dayMenu = DayMenu.objects.filter(braekfast=meal) | DayMenu.objects.filter(lanch=meal) | DayMenu.objects.filter(dinner=meal) | DayMenu.objects.filter(snack=meal)
            dayMenu = dayMenu[0]
            dayMenu.kkal += meal.kkal
            dayMenu.proteins += meal.proteins
            dayMenu.fats += meal.fats
            dayMenu.carbohydrates += meal.carbohydrates
            dayMenu.save()
            
            return redirect('food_dairy_by_date', day.day.strftime("%Y-%m-%d"))
    else:
        #print(newNote.mealType)
        form1 = FoodDairyNoteForm(instance = newNote)
        form2 = DayNoteForm(instance = dayNote)
    #return render(request, "trainer_create_update.html", {'form1': form1, 'form2': form2, 'activeTrainer': True})
    return render(request, 'food_dairy/add_note.html', {'form1': form1, 'form2': form2, "activeFood": True})

def save_comment(request, day=None):
    text = request.GET.get('comment', None)
    note_id = request.GET.get('note_id', None)
    if text:
        comment = Comment.objects.create(
            author = request.user,
            created_by = timezone.now(),
            text = text,
            foodNote = FoodDairyNote.objects.get(id=int(note_id))
        )
        response = {
            'comment': {
                'author': comment.author.__str__(),
                'created_by': comment.created_by,
                'text': comment.text
            }
        }

    else:
        response = {
            'error': 'Поле ввода пустое. Введите комментарий чтобы его отправить'
        }
    return JsonResponse(response)

def save_note(request, day=None):
    date = request.POST.get('date', None)
    meal = request.POST.get('meal', None)
    image = request.POST.get('image', None)
    print(settings.MEDIA_ROOT)
    imagef = request.FILES.get('imagef')
    kkal = request.POST.get('kkal', None)
    proteins = request.POST.get('proteins', None)
    fats = request.POST.get('fats', None)
    carbohydrates = request.POST.get('carbohydrates', None)
    comment = request.POST.get('comment', None)
    if date:
        dayNote = DayNote.objects.filter(user=request.user, day=datetime.strptime(date, '%Y-%m-%d').date())
        if len(dayNote) == 0:
            dayNote = DayNote.objects.create(
                day = datetime.strptime(date, '%Y-%m-%d').date(),
                user = request.user
            )
        else:
            dayNote = dayNote[0]
        if meal and (image or (kkal and proteins and fats and carbohydrates)):
            if imagef:
                
                fs = FileSystemStorage(
                    location=str(settings.MEDIA_ROOT)+'/fooddairy/assets/media/',
                    base_url='/fooddairy/assets/media/'
                )
                file = fs.save(imagef.name, imagef)
                url = fs.url(file)
            else:
                url = None
            note = FoodDairyNote.objects.create(
                day = dayNote,
                mealType = MealType.objects.get(pk=int(meal)),
                image = url,
                kkal = kkal,
                proteins = proteins,
                fats = fats,
                carbohydrates = carbohydrates
            )

            if comment:
                comment = Comment.objects.create(
                    author = request.user,
                    created_by = timezone.now(),
                    text = comment,
                    foodNote = note
                )
        response = {
            'day': {
                'day': dayNote.day.strftime('%Y-%m-%d')
            },
            'note': {
                'mealType': note.mealType.__str__(),
                'image': note.image.url,
                'kkal': note.kkal,
                'proteins': note.proteins,
                'fats': note.fats,
                'carbohydrates': note.carbohydrates,
            },
            'comment': {
                'author': comment.author.__str__(),
                'created_by': comment.created_by,
                'text': comment.text
            }
        }

    else:
        response = {
            'error': 'Поле ввода пустое. Введите комментарий чтобы его отправить'
        }
    return JsonResponse(response)
