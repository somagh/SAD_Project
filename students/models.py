from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class Student(models.Model):
    user = models.OneToOneField(to=User, on_delete=CASCADE)
    studentID = models.CharField(max_length=12, primary_key=True)

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def email(self):
        return self.user.email

    @property
    def username(self):
        return self.user.username


class Employee(models.Model):
    user = models.OneToOneField(to=User)
    position = models.ForeignKey(to='Position')


class Position(models.Model):
    name = models.CharField(max_length=40)
