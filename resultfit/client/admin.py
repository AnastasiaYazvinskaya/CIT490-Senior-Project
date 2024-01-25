from django.contrib import admin
from .models import *

class ClientTrainerAdmin(admin.ModelAdmin):
    list_display = ('client', 'trainer', 'active')
admin.site.register(ClientTrainer, ClientTrainerAdmin)