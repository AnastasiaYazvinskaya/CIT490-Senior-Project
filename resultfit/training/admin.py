from django.contrib import admin
from .models import *

class ExercisesInline(admin.StackedInline):
    model = TrainingExercise
    extra = 0

class TrainingExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'training', 'exercise', 'repeatNum', 'timesNum')
admin.site.register(TrainingExercise, TrainingExerciseAdmin)

class TrainingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'weekDay', 'time')
    inlines = [ExercisesInline]
admin.site.register(Training, TrainingAdmin)

class TrainingNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'day', 'user', 'training')
admin.site.register(TrainingNote, TrainingNoteAdmin)