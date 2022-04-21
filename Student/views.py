from django.shortcuts import render
from SuperAdmin.models import *


# Create your views here.
def dashboard(request):
    user = request.user
    quizes = Quiz.objects.filter(batch = user.batch,post=True)


    return render(request,"Student/dashboard.html",{"quizes":quizes,"user":user})


def quizview(request,id):
    quiz = Quiz.objects.get(id = id)

    return render(request,"Student/quizview.html",{"quiz":quiz})