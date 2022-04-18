from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout



from .models import *


# Create your views here.
def loginPage(request):
    if(request.user.is_authenticated):
        pass
    else:
        if(request.method == "POST"):
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(email=email,password = password)
            if(user is not None):
                login(request,user)
                if(user.isStudent == True):
                    pass
                elif(user.isFaculty == True):
                    pass
                elif(user.isAdmin == True):
                    pass
                