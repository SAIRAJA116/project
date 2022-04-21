from django.urls import path

from . import views
app_name="SuperAdmin"

urlpatterns = [
      path("dashboard/",views.dashboard,name="dashboard"),
      path("setup/",views.setup,name="setup"),
      path("customizeCourse/",views.customizeCourse,name="customizeCourse"),
      path('createquiz/<int:id>',views.createQuiz,name="createQuiz")
]
