from django.contrib import admin
from .models import *

class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
admin.site.register(ActivityType, ActivityTypeAdmin)

admin.site.register(PurposeType)
