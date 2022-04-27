from django.urls import path

from . import views
app_name="App"

urlpatterns = [
   path("",views.loginPage,name="loginPage"),
   path("logoutuser/",views.logoutuser,name="logoutuser") ,
   path("forgotpassword/",views.forgotpassword,name="forgotpassword"),
   path("validateotp/<str:email>/<str:otp>",views.validateOTP,name="validateotp"),
   path("password changed/",views.passwordChanged,name="passwordchanged")
]
