from django.shortcuts import render,redirect
import csv
from django.contrib.auth.hashers import check_password,make_password
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse


from App.models import NewUser,Batch
from .models import Group,Course,FacultyDealsWith,Csv, Quiz,Question,Answer,Result,QuizSeen
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
    students = NewUser.objects.filter(isStudent=True).order_by("roll")
    faculty =  NewUser.objects.filter(isFaculty=True).order_by("roll")
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


def deleteuser(request,id):
    try:
        user = NewUser.objects.get(id=id)
        user.delete()
        messages.error(request,"User deleted")
    except:
        pass
        print("erroroccured")
    return redirect("SuperAdmin:setup")

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
                    print(answer_text)
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



def quizresult(request,id):
    quiz = Quiz.objects.get(id=id)
    students = NewUser.objects.filter(batch=quiz.batch)
    results = Result.objects.filter(quiz=quiz)
    total = len(students)
    completed = len(results)
    notcompleted = total - completed

    return render(request,"SuperAdmin/quizresult.html",{"quiz":quiz,"results":results,"total":total,"completed":completed,"notcompleted":notcompleted,"students":students})


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
        return redirect("SuperAdmin:myAccount")
    return render(request,"SuperAdmin/myAccount.html",{"user":user})



def deleteavatar(request):
    pass
    user = request.user
    user.avatar = None
    user.save()
    return redirect("SuperAdmin:myAccount") 




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
