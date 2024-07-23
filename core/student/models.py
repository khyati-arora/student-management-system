from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.

class CustomUser(AbstractUser):
    user_type_data = ((1, "Staff"), (2, "Student"), (3,"Admin"))
    user_type = models.CharField(default=3, choices=user_type_data, max_length=10) 
    name = models.CharField(max_length=100)
    address = models.TextField()   
    gender = models.CharField(max_length=50)
  

class Course(models.Model):
    id = models.AutoField(primary_key=True)  
    course_name = models.CharField(max_length=255,unique=True)
   

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    basic_details = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    guardian = models.CharField(max_length=100)
    
class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    basic_details = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    salary = models.CharField(max_length=30)
   
class Results(models.Model):
     student = models.ForeignKey(Students,on_delete=models.CASCADE)
     course = models.ForeignKey(Course,on_delete=models.CASCADE)
     grade = models.CharField(max_length=10)

     class Meta:
         unique_together = ('student', 'course')

class Attendance(models.Model):
    student = models.ForeignKey('Students', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    class Meta:
        unique_together = ('student', 'course', 'date')
    

