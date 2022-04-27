from django.shortcuts import render,redirect
from SuperAdmin.models import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password,make_password
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def dashboard(request):
    user = request.user
    quizes = Quiz.objects.filter(batch = user.batch,post=True)
    results = Result.objects.filter(student = request.user)
    quizseen = QuizSeen.objects.filter(student = request.user)
    malpractised = []
    result_id = []
    for i in results:
        result_id.append(i.quiz.id)

    for i in quizseen:
        flag=True
        for j in results:
            if(i.quiz==j.quiz):
                flag=False
                break
        if(flag):
            malpractised.append(i)
    not_answered = []
    for i in quizes:
        flag=False
        for j in quizseen:
            if(i == j.quiz):
                flag=True
                break
        if(flag == False ):
            not_answered.append(i)


    
    return render(request,"Student/dashboard.html",{"quizes":not_answered,"user":user,"results":results,"malpractised":malpractised})


def quizview(request,id):
    quiz = Quiz.objects.get(id = id)
    quizseen = QuizSeen(quiz=quiz,student=request.user,seen=True)
    quizseen.save()
    
    if(request.method=="POST"):
        count=0
        for question in quiz.get_questions():
            ans = request.POST.get("question"+str(question.id)) 
            if(ans is not None):  
                answer = Answer.objects.get(id=ans)
                if(answer.correct == True):
                    count+=1
        result = Result(quiz=quiz,student = request.user,marks=count)
        result.save()
        messages.success(request,"Your Score is "+str(count)+" / "+str(quiz.no_of_questions))
        return redirect("Student:dashboard")
        


    return render(request,"Student/quizview.html",{"quiz":quiz})

def myAccount(request):
    user = request.user
    if(request.method=="POST" or request.FILES):
        pass
        if("name" in request.POST):
            name = request.POST.get('name')
            user.name = name
            user.save()
        elif("resetpassword" in request.POST):
            oldpassword = request.POST.get("oldpassword")
            newpassword = request.POST.get("newpassword")
            if(check_password(oldpassword,user.password)):
                user.password=make_password(newpassword)
                user.save()
                logout(request)
                return redirect("App:loginPage")
        elif('changeimage' in request.POST):
            avatar = request.FILES.get("avatar")
            user.avatar = avatar
            user.save()
        return redirect("Student:myAccount")
    return render(request,"Student/myAccount.html",{"user":user})



def deleteavatar(request):
    pass
    user = request.user
    user.avatar = None
    user.save()
    return redirect("Student:myAccount")