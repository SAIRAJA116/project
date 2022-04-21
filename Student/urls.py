from django.urls import path

from . import views
app_name="Student"

urlpatterns = [
    path('dashboard/',views.dashboard,name="dashboard"),
    path('quizview/<int:id>',views.quizview,name="quizview")
]
