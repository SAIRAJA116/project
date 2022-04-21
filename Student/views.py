from django.shortcuts import render,redirect
from SuperAdmin.models import *
from django.contrib import messages

# Create your views here.
def dashboard(request):
    user = request.user
    quizes = Quiz.objects.filter(batch = user.batch,post=True)


    return render(request,"Student/dashboard.html",{"quizes":quizes,"user":user})


def quizview(request,id):
    quiz = Quiz.objects.get(id = id)
    
    if(request.method=="POST"):
        count=0
        for question in quiz.get_questions():
            ans = request.POST.get("question"+str(question.id)) 
            if(ans is not None):  
                answer = Answer.objects.get(id=ans)
                if(answer.correct == True):
                    count+=1
        messages.success(request,"Your Score is "+str(count)+" / "+str(quiz.no_of_questions))
        return redirect("Student:dashboard")
        


    return render(request,"Student/quizview.html",{"quiz":quiz})

