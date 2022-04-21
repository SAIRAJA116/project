from contextlib import redirect_stderr
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse



from .models import *


# Create your views here.
def loginPage(request):
    # if(request.user.is_authenticated):
    #     pass
    # else:
    if(request.method == "POST"):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email,password = password)
        print(user)
        if(user is not None):
            login(request,user)
            if(user.isStudent == True):
                return redirect("Student:dashboard")
            elif(user.isFaculty == True):
                return HttpResponse("Faculty")
            elif(user.isAdmin == True):
                return redirect("SuperAdmin:dashboard")
 
    return render(request,"App/loginpage.html")
                