from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from user.models import Profile
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

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
def food_dairy(request, day=None):
    dayNotes = DayNote.objects.filter(user = request.user).order_by('-day')
    if day is None:
        day = dayNotes[0]
    else:
        day = dayNotes.filter(day = datetime.strptime(day, '%Y-%m-%d'))[0]
        print('day', day.day)
    
    notesQ = day.foodday.all()#.order_by('-mealType__id')
    notes = {}
    notes['notes'] = notesQ.values()
    notes['day'] = day.day#.strftime('%Y-%m-%d')
    for idy, note in enumerate(notes['notes']):
        note['comments'] = notesQ[idy].foodnote.all().order_by('-created_by')
        note['image_url'] = notesQ[idy].image.url
        note['mealType'] = notesQ[idy].mealType.name
    print('notes', notes)
    
    return render(request, 'food_dairy/dairy.html', {"days": dayNotes, "notes": notes, "activeFood": True, "activeDay": day.day})

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
