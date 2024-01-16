from django.contrib import admin
from .models import *

admin.site.register(Profile)

class PrepareUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstName', 'lastName', 'email', 'user', 'active')
admin.site.register(PrepareUser, PrepareUserAdmin)