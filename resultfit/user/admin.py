from django.contrib import admin
from .models import *

class FileInline(admin.StackedInline):
    model = File
    extra = 0

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sex', 'purpose')
    inline = [FileInline]
admin.site.register(Profile, ProfileAdmin)