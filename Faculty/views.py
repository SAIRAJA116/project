from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import check_password,make_password
import csv
from django.http import HttpResponse
# Create your views here.

from App.models import *
from SuperAdmin.models import *


def dashboard(request):
    user = request.user
    courses = FacultyDealsWith.objects.filter(faculty=user)
    batch = Batch.objects.all()
    draft_quizes = Quiz.objects.filter(post = False,createdBy=user).order_by("-published")
    quizes = Quiz.objects.filter(post = True,createdBy=user).order_by("-published")

    if(request.method=="POST"):
        name=request.POST.get("quizname")
        description = request.POST.get("description")
        no_of_questions = request.POST.get("question_no")
        time = request.POST.get("time")
        group = request.POST.get("group")
        batch = request.POST.get("batch")
        try:
            quiz = Quiz(name=name.rstrip(' '),description=description,no_of_questions=no_of_questions,time=time,group=Group.objects.get(id=group),batch=Batch.objects.get(id=batch),createdBy=request.user)
            quiz.save()
        except:
            pass
        
        return redirect("Faculty:dashboard")


    return render(request,"Faculty/dashboard.html",{"posted":quizes,"drafted":draft_quizes,"courses":courses,"batch":batch})



def createQuiz(request,id):
    try:
        quiz = Quiz.objects.get(id=id,createdBy = request.user)
        question_count = quiz.no_of_questions
        if(request.method == "POST" or request.FILES):
            if(quiz.drafted):
                pass
                i=1
                for question in quiz.get_questions():
                    question_text = request.POST.get("question"+str(i))
                    question.question_text = question_text
                    question.save()
                    j=1
                    for answer in question.get_answers():
                        answer_text = request.POST.get("answer"+str(j)+"-"+str(i))
                        answer_crr  = request.POST.get("anscrr"+str(j)+"-"+str(i))
                        answer.answer_text = answer_text
                        print(answer.answer_text," - ",answer_text)
                        if(answer_crr == "on"):
                            answer.correct = True
                        else:
                            answer.correct = False
                        answer.save()
                        print(answer.answer_text)
                        j+=1
                    i+=1
            else:
                for i in range(1,question_count+1):
                    pass
                    question_text = request.POST.get("question"+str(i))
                    question = Question(quiz = quiz,question_text=question_text)
                    question.save()
                    for j in range(1,5):
                        pass
                        answer_text = request.POST.get("answer"+str(j)+"-"+str(i))
                        print(answer_text)
                        answer_crr  = request.POST.get("anscrr"+str(j)+"-"+str(i))
                        if(answer_crr == "on"):
                            answer = Answer(question=question,answer_text = answer_text,correct = True)
                            answer.save()
                        else:
                            answer = Answer(question=question,answer_text = answer_text,correct = False)
                            answer.save()
                quiz.drafted = True
                quiz.save()
            
            postorsave = request.POST.get("postorsave")
            if(postorsave == "post"):
                quiz.post = True
                quiz.save()
            return redirect("Faculty:dashboard")
    except:
        return render("Faculty:dashboard") 
    return render(request,"Faculty/createQuiz.html",{"quiz":quiz})


def quizresult(request,id):
    try:
        quiz = Quiz.objects.get(id=id,createdBy=request.user)
        students = NewUser.objects.filter(batch=quiz.batch)
        results = Result.objects.filter(quiz=quiz)
        total = len(students)
        completed = len(results)
        notcompleted = total - completed

        return render(request,"Faculty/quizresult.html",{"quiz":quiz,"results":results,"total":total,"completed":completed,"notcompleted":notcompleted,"students":students})
    except:
        return redirect("Faculty:dashboard")


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
        return redirect("Faculty:myAccount")
    return render(request,"Faculty/myAccount.html",{"user":user})



def deleteavatar(request):
    pass
    user = request.user
    user.avatar = None
    user.save()
    return redirect("Faculty:myAccount") 



def getMarks(student_id,quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    student = NewUser.objects.get(id=student_id)
    result = Result.objects.filter(quiz=quiz,student = student)
    if(len(result)==0):
        quizseen = QuizSeen.objects.filter(quiz=quiz,student = student)
        if(len(quizseen)==0):
                return None
        else:
                return "Malpracticed"
    return result[0].marks


def export_csv(request,id):
    quiz = Quiz.objects.get(id=id)
    students = NewUser.objects.filter(batch = quiz.batch ).order_by('roll')
    results = Result.objects.filter(quiz=quiz).order_by('student__roll')
    print(students)
    print(results)

    response = HttpResponse(content_type = "text/csv")
    response['Content-Desposition'] = 'attachment; filename="quizReport.csv"'

    writer = csv.writer(response)
    writer.writerow(['','QuizName','',quiz.name])
    for i in range(2):
        writer.writerow(['','','',''])
    writer.writerow(['','Publish Time','',quiz.published.strftime("%Y-%m-%d %I:%M %p")])
    for i in range(2):
        writer.writerow([''])
    writer.writerow(['S.NO','ROLL','NAME','MARKS'])
    i=1
    for student in students:
        marks = getMarks(student.id,quiz.id)
        if(marks):
            writer.writerow([i,str(student.roll),student.name,marks])
        else:
            writer.writerow([i,str(student.roll),student.name,'not answered'])
        i+=1
    response['Content-Disposition'] = 'attachment; filename='+quiz.name+'.csv'
    return response 