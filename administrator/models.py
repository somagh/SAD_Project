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
    name = models.CharField(max_length=100,verbose_name='نام')
    first_step = models.ForeignKey(to='Step', related_name='+',verbose_name='گام اولیه',blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'فرایند'


class Step(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')
    description = models.TextField(verbose_name='نام')
    has_payment = models.BooleanField(verbose_name='امکان پرداخت')
    needs_clarification = models.BooleanField(verbose_name='امکان درخواست توضیح')
    process = models.ForeignKey(to=Process, related_name='steps',verbose_name='فرایند')
    pass_step = models.ForeignKey(to='Step', null=True, blank=True, related_name='+',verbose_name='گام بعدی در صورت موفقیت')
    fail_step = models.ForeignKey(to='Step', null=True, blank=True, related_name='+',verbose_name='گام بعدی در صورت شکست')
    position = models.ForeignKey(to=Position, related_name='steps',verbose_name='سمت مربوطه')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'گام'
