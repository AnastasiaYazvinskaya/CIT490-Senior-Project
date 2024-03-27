from django.contrib import admin
from .models import *

class PrepareUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstName', 'lastName', 'email', 'user', 'active')
admin.site.register(PrepareUser, PrepareUserAdmin)

class QualificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'type')
admin.site.register(Qualification, QualificationAdmin)