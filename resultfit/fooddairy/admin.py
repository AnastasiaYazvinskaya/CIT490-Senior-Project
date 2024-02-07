from django.contrib import admin
from .models import *

class FoodDairyGeneralAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'kkal', 'proteins', 'fats', 'carbohydrates')
admin.site.register(FoodDairyGeneral, FoodDairyGeneralAdmin)

class DayMenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'day', 'user')
admin.site.register(DayMenu, DayMenuAdmin)

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'author', 'text')
admin.site.register(Comment, CommentAdmin)

class FoodDairyNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'mealType')
    inlines = [CommentInline]
admin.site.register(FoodDairyNote, FoodDairyNoteAdmin)

class FoodDairyNoteInline(admin.StackedInline):
    model = FoodDairyNote
    extra = 0

class DayNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'day', 'user')
    inlines = [FoodDairyNoteInline]
admin.site.register(DayNote, DayNoteAdmin)

