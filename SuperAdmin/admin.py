from atexit import register
from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Group)
admin.site.register(Course)
admin.site.register(FacultyDealsWith)
admin.site.register(Csv)