from atexit import register
from django.contrib import admin
from .models import *
# Register your models here.

class UserAdminConfig(admin.ModelAdmin):
    ordering=("roll","email")
    list_display = ('email','roll','isStudent','isFaculty','isAdmin')
    search_fields = ('email','roll','name')

admin.site.register(NewUser,UserAdminConfig)
admin.site.register(Batch)
admin.site.register(OTPContainer)