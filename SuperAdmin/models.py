from turtle import onclick
from django.db import models
import os

from App.models import NewUser

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