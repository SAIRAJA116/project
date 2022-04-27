from django.db import models
from django.utils.translation import gettext_lazy
from django.utils import timezone
import os
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from datetime import datetime
from PIL import Image  


class Batch(models.Model):
    batchname = models.CharField(max_length=300)

    def __str__(self):
        return self.batchname

# Create your models here.
class CustomAccountManager(BaseUserManager):
    def create_user(self,email,roll,password,**other_fields):
        if not email:
            raise ValueError(gettext_lazy("You must provide an email"))
        email = self.normalize_email(email)
        user = self.model(email=email,roll = roll,**other_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self,email,roll,password,**other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email,roll,password,**other_fields)


def get_avataar_path(instance,avatar):
    pass
    return os.path.join("Avatar/{0}/{1}".format(instance.email,instance.avatar))

class NewUser(AbstractBaseUser,PermissionsMixin):
    username = None
    email = models.EmailField(gettext_lazy("email address"),unique=True)
    roll = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=200,blank=True)
    mobile = models.CharField(max_length=12,blank=True)
    isStudent = models.BooleanField(default = False)
    isFaculty = models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(default=timezone.now)
    avatar = models.ImageField(upload_to=get_avataar_path, blank=True)
    batch =  models.ForeignKey(Batch,on_delete=models.CASCADE,blank=True,null=True)

    objects = CustomAccountManager()


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['roll','name']

    def __str__(self):
        return self.email+"("+self.roll+")"

class OTPContainer(models.Model):
    otp = models.CharField(max_length=10)
    

    