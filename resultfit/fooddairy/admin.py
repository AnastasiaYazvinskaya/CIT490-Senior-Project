from django.contrib import admin
from .models import *

class FoodDairyGeneralAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'kkal', 'proteins', 'fats', 'carbohydrates')
admin.site.register(FoodDairyGeneral, FoodDairyGeneralAdmin)