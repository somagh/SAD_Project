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

    class Meta:
        verbose_name = 'دانشجو'

class Employee(models.Model):
    user = models.OneToOneField(to=User)
    position = models.ForeignKey(to='Position')

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

    class Meta:
        verbose_name = 'کارمند دون‌پایه'

class Position(models.Model):
    name = models.CharField(max_length=40, verbose_name='نام')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'سمت'


class Process(models.Model):
    name = models.CharField(max_length=100)
    first_step = models.ForeignKey(to='Step', related_name='+')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'فرایند'


class Step(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    has_payment = models.BooleanField()
    needs_clarification = models.BooleanField()
    process = models.ForeignKey(to=Process, related_name='steps')
    pass_step = models.ForeignKey(to='Step', null=True, blank=True, related_name='+')
    fail_step = models.ForeignKey(to='Step', null=True, blank=True, related_name='+')
    position = models.ForeignKey(to=Position, related_name='steps')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'گام'
