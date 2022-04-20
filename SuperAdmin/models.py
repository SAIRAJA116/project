from tokenize import blank_re
from turtle import onclick
from django.db import models
import os

from App.models import NewUser,Batch

# Create your models here.
class Group(models.Model):
      groupName = models.CharField(max_length=200,unique=True)

      def __str__(self):
            return str(self.groupName)

class Course(models.Model):
      courseName = models.CharField(max_length=100)
      group = models.ForeignKey(Group,on_delete=models.CASCADE)

      class Meta:
        unique_together = (('courseName','group'))

      def __str__(self):
            return self.courseName+"--"+self.group.groupName

class FacultyDealsWith(models.Model):
      courseid = models.ForeignKey(Course,on_delete=models.CASCADE)
      faculty = models.ForeignKey(NewUser,on_delete = models.CASCADE)

      def __str__(self):
            return self.courseid.courseName+'  -  '+self.faculty.name

def csv_path(instance):
    return os.path.join("csvs/{0}".format(instance.doc))


class Csv(models.Model):
    doc = models.FileField(upload_to="csv_path")
    
    def __str__(self):
        return self.doc

    def delete(self,using=None,keep_parents=False):
        self.doc.storage.delete(self.doc.name)
        super().delete()


class Quiz(models.Model):
    pass
    name = models.CharField(max_length=400)
    description = models.CharField(max_length=100)
    no_of_questions = models.IntegerField(blank=True)
    time = models.IntegerField(help_text="Time duration in number of minutes")
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

    def get_questions(self):
        return self.question_set.all()

def get_question_imagepath(instance,image):
    return os.path.join("Quizs/{0}/{1}".format(instance.quiz.name,instance.image))

class Question(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    question_text = models.CharField(max_length=1000)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=get_question_imagepath,blank=True)

    def __str__(self):
        return self.quiz.name
    
    def get_answers(self):
        return self.answer_set.all()

def get_answer_imagepath(instance,image):
    return os.path.join("Quizs/{0}/{1}".format(instance.question.quiz.name,instance.image))


class Answer(models.Model):
    answer_text = models.TextField()
    image = models.ImageField(upload_to=get_answer_imagepath,blank=True)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.question.id+" "+self.answer_text+" "+str(self.correct)
    
    
class Result(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    student = models.ForeignKey(NewUser,on_delete=models.CASCADE)
    marks = models.IntegerField()

    def __str__(self):
        return self.quiz.name+" "+self.student.name+" "+str(self.marks)
