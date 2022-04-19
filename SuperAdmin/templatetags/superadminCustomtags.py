from django import template
from SuperAdmin.models import *
from App.models import *

register = template.Library()

@register.simple_tag
def getFaculty(course):
      faculty = FacultyDealsWith.objects.filter(courseid = course)
      if(len(faculty)>0):
            return faculty[0]
      else:
            return None