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


@register.simple_tag
def getMarks(student_id,quiz_id):
      quiz = Quiz.objects.get(id=quiz_id)
      student = NewUser.objects.get(id=student_id)
      print(quiz)
      print(student)
      result = Result.objects.filter(quiz=quiz,student = student)
      if(len(result)==0):
            quizseen = QuizSeen.objects.filter(quiz=quiz,student = student)
            if(len(quizseen)==0):
                  return None
            else:
                  return "Malpracticed"
      return result[0].marks