from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(to=User)
    studentID = models.CharField(max_length=12)


class Employee(models.Model):
    user = models.OneToOneField(to=User)
    position = models.ForeignKey(to='Position')


class Position(models.Model):
    name = models.CharField(max_length=40)
