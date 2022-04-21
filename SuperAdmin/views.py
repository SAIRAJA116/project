from typing import no_type_check
from django.shortcuts import render,redirect
import csv
from django.contrib.auth.hashers import check_password,make_password
from django.contrib import messages

from App.models import NewUser,Batch
from .models import Group,Course,FacultyDealsWith,Csv, Quiz,Question,Answer
# Create your views here.

def dashboard(request):
    
    groups = Group.objects.all()
    batch = Batch.objects.all()
    draft_quizes = Quiz.objects.filter(post = False).order_by("-published")
    quizes = Quiz.objects.filter(post = True).order_by("-published")

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
        
        return redirect("SuperAdmin:dashboard")


    return render(request,"SuperAdmin/dashboard.html",{"posted":quizes,"drafted":draft_quizes,"groups":groups,"batch":batch})


def setup(request):
    groups = Group.objects.all()
    students = NewUser.objects.filter(isStudent=True)
    faculty =  NewUser.objects.filter(isFaculty=True)
    batch = Batch.objects.all()

    if(request.method == "POST"):
        if("add-by-csv" in request.POST or request.FILES):
            o=Csv(doc=request.FILES.get("doc"))
            o.save()
            with open(o.doc.path,'r') as f:
                reader = csv.reader(f)
                count=0
                for i,row in enumerate(reader):
                    if(i==0):
                        pass
                    else:
                        try:
                            batch = Batch.objects.get(batchname = row[3])
                            user = NewUser(email=row[0],roll=row[1],name = row[2],batch=batch,mobile=row[4],password = make_password(row[1]) ,isStudent = True)
                            user.save()
                            count+=1
                        except:
                            messages.error(request,"Error occured while creating an user of email "+row[0]+" may be error occured because of batchname or an email")
            o.delete()
            if(count!=0):
                messages.success(request,"Total "+str(count)+" users have been created")
            return redirect("SuperAdmin:setup")
        elif("addstudent" in request.POST):
            pass
            name = request.POST.get("name")
            mobile = request.POST.get("mobile")
            email = request.POST.get("email")
            roll = request.POST.get("roll")
            batch = request.POST.get("batch")
            try:
                user = NewUser(email=email,roll=roll,name=name,mobile=mobile,isStudent = True,batch=Batch.objects.get(id=batch),password=make_password(roll))
                user.save()
                messages.success(request,"Student with email "+email+" have been added.")
            except:
                messages.error(request,"Error occured while adding the Student with email "+email+" .")

        elif("addfaculty" in request.POST):
            name = request.POST.get("name")
            mobile = request.POST.get("mobile")
            email = request.POST.get("email")
            roll = request.POST.get("roll")
            try:
                user = NewUser(email=email,roll=roll,name=name,mobile=mobile,isFaculty = True,password=make_password(roll))
                user.save()
                messages.success(request,"Faculty with email "+email+" have been added.")
            except:
                messages.error(request,"Error occured while adding the Faculty with email "+email+" .")


            
    return render(request,"SuperAdmin/setup.html",{"groups":groups,"students":students,"batch":batch,"faculty":faculty})

def customizeCourse(request):
    courses = Course.objects.all()
    groups = Group.objects.all()
    if(request.method=="POST"):
        if("addcourse" in request.POST):
            courseName =  request.POST.get("course")
            group = request.POST.get("group")
            course = Course(courseName = courseName,group = Group.objects.get(id=group))
            course.save()      
        elif("addfaculty" in request.POST):
            course = request.POST.get("course")
            email = request.POST.get("email")
            roll=request.POST.get("roll")
            faculty = NewUser.objects.get(email=email,roll=roll)
            link = FacultyDealsWith(faculty=faculty,courseid=Course.objects.get(id=course))
            link.save()
        elif("editfaculty" in request.POST):
            course = Course.objects.get(id=request.POST.get("course"))
            currfaculty = NewUser.objects.get(id = request.POST.get("currfaculty"))
            email = request.POST.get("email")
            roll=request.POST.get("roll")
            faculty = NewUser.objects.get(email=email,roll=roll)
            link = FacultyDealsWith.objects.get(courseid = course,faculty = currfaculty)
            link.faculty = faculty
            link.save()
        return redirect("SuperAdmin:customizeCourse")
    
    return render(request,"SuperAdmin/customizecourse.html",{"courses":courses,"groups":groups})

def createQuiz(request,id):
    quiz = Quiz.objects.get(id=id)
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
                    if(answer_crr == "on"):
                        answer.correct = True
                    else:
                        answer.correct = False
                    answer.save()
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
        print(postorsave)
        if(postorsave == "post"):
            quiz.post = True
            quiz.save()
        return redirect("SuperAdmin:dashboard")
        
                
                    
            
            

    return render(request,"SuperAdmin/createQuiz.html",{"quiz":quiz})