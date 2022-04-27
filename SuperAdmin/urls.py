from django.urls import path

from . import views
app_name="SuperAdmin"

urlpatterns = [
      path("dashboard/",views.dashboard,name="dashboard"),
      path("setup/",views.setup,name="setup"),
      path("deleteuser/<int:id>",views.deleteuser ,name="deleteuser"),
      path("customizeCourse/",views.customizeCourse,name="customizeCourse"),
      path('createquiz/<int:id>',views.createQuiz,name="createQuiz"),
      path("quizresult/<int:id>",views.quizresult,name="quizresult"),
      path("myAccount/",views.myAccount,name="myAccount"),
      path("deleteavatar/",views.deleteavatar,name="deleteavatar"),
      path("export_csv/<int:id>",views.export_csv,name="export_csv")
]
