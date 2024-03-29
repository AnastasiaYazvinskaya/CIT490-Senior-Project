from django.contrib import admin
from .models import *

class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'active')
admin.site.register(ActivityType, ActivityTypeAdmin)

class PurposeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
admin.site.register(PurposeType, PurposeTypeAdmin)

class PrivacyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'active')
admin.site.register(PrivacyType, PrivacyTypeAdmin)

class UnitTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'full_name', 'description', 'active')
admin.site.register(UnitType, UnitTypeAdmin)

class MealTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
admin.site.register(MealType, MealTypeAdmin)

class FileTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
admin.site.register(FileType, FileTypeAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'kkal', 'proteins', 'fats', 'carbohydrates', 'baseUnit', 'active')
admin.site.register(Product, ProductAdmin)

class LargeZoneTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'active')
admin.site.register(LargeZoneType, LargeZoneTypeAdmin)

class ZoneTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'active')
admin.site.register(ZoneType, ZoneTypeAdmin)

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'zoneType')
admin.site.register(Exercise, ExerciseAdmin)

