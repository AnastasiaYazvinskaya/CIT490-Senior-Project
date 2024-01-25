from django.contrib import admin
from .models import *

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sex', 'purpose')
admin.site.register(Profile, ProfileAdmin)