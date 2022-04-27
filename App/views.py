from contextlib import redirect_stderr
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
import random


#dependies required for HTML email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string #This is used for convert the html in to sharable string format
from django.utils.html import strip_tags
#################################

from .models import *


# Create your views here.
def loginPage(request):
    if(request.user.is_authenticated):
        pass
        user = request.user
        if(user.isAdmin):
            return redirect("SuperAdmin:dashboard")
        elif(user.isStudent):
            return redirect("Student:dashboard")
        elif(user.isFaculty):
            return redirect("Faculty:dashboard")
    else:
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
                    return redirect("Faculty:dashboard")
                elif(user.isAdmin == True):
                    return redirect("SuperAdmin:dashboard")
 
    return render(request,"App/loginpage.html")
                

def logoutuser(request):
    pass
    logout(request)
    return redirect("App:loginPage")

def forgotpassword(request):
    if(request.user.is_authenticated):
        pass
        user = request.user
        if(user.isAdmin):
            return redirect("SuperAdmin:dashboard")
        elif(user.isStudent):
            return redirect("Student:dashboard")
        elif(user.isFaculty):
            pass
    else:
        if(request.method == "POST"):
            email = request.POST.get("email")
            try:
                user = NewUser.objects.get(email=email)
                otp = make_password(generateOTP(user.email,user.name))
                print(otp)
                o = OTPContainer(otp = otp)
                o.save()
                return redirect("App:validateotp",email=email,otp=str(o.id))
            except:
                pass
                messages.error(request,"User with this email address does not exits, please make sure wheather you are using valid email or not")
        return render(request,"App/forgotpassword.html")


def generateOTP(email,name):
    series = "0123456789"
    otp = "".join(random.sample(series,6))
    # -----------------Sending OTP to Email ---------------------

    #creating the html email
    html_content = render_to_string("App/OTP.html",{"name":name,"otp":otp})
    text_content = strip_tags(html_content)
    email_obj=EmailMultiAlternatives(
        #subject
        "BVCEC Exam Support",
        #content
        text_content,
        #from email
        "bvcecexam@gmail.com",
        #to email
        [email]
    )
    email_obj.attach_alternative(html_content,"text/html")
    email_obj.send()
    # -----------------------------------------------------------
    return otp


def validateOTP(request,email,otp):
    pass
    if(request.method == "POST"):
        pass
        userotp = request.POST.get("otp")
        password = request.POST.get("p1")
        try:
            if(check_password(userotp,OTPContainer.objects.get(id=otp).otp)):
                print("in")
                user = NewUser.objects.get(email=email)
                user.password = make_password(password)
                user.save()
                OTPContainer.objects.get(id=otp).delete()
                print("Iam in")
                return redirect("App:passwordchanged")
            else:
                messages.error(request,"You have entered the wrong otp")
        except:
            messages.error(request,"Bad request")
    print(" I am here ")
    return render(request,"App/validation.html")

def passwordChanged(request):
    return render(request,"App/passwordchanged.html")