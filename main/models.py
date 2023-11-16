from __future__ import unicode_literals
from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Register(models.Model):
    name = models.TextField() 
    email = models.EmailField()
    password = models.CharField(max_length=10)
    
    class Meta:
        db_table="Login"

class Main (models.Model):
    
    name = models.TextField()
    about = models.TextField(default="-")
    
    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.title

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, related_name='students')

    def __str__(self):
        return self.user.username

class FacultyMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.user.username

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title