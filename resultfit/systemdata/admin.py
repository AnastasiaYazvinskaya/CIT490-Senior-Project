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

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'kkal', 'proteins', 'fats', 'carbohydrates', 'baseUnit', 'active')
admin.site.register(Product, ProductAdmin)

