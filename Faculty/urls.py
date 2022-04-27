from django.urls import path

from . import views
app_name="Faculty"

urlpatterns = [
    path("dashboard/",views.dashboard,name="dashboard"),
    path('createquiz/<int:id>',views.createQuiz,name="createQuiz"),
    path("quizresult/<int:id>",views.quizresult,name="quizresult"),
    path("myAccount/",views.myAccount,name="myAccount"),
    path("deleteavatar/",views.deleteavatar,name="deleteavatar"),
    path("export_csv/<int:id>",views.export_csv,name="export_csv")

]
