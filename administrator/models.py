from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class PaymentTransaction:
    def __init__(self, price, pursuit, date, concern):
        self.price = price
        self.pursuit = pursuit
        self.date = date
        self.concern = concern


class Student(models.Model):
    user = models.OneToOneField(to=User, on_delete=CASCADE)
    studentID = models.CharField(max_length=12, primary_key=True)

    def __str__(self):
        return '{} {} {}'.format(self.studentID, self.first_name, self.last_name)

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

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_payment_transactions(self):
        transactions = []
        for process_instance in self.process_instances.all():
            transactions += process_instance.get_payment_transactions()
        return transactions

    def notify(self,subject,message):
        print(subject)
        print(message)
        send_mail(subject, message, from_email="sad@project.com", recipient_list=[self.user.email],
                  fail_silently=False)

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

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_related_step_instances(self):
        from student.models import StepInstance, Status

        out = []
        for step_instance in StepInstance.objects.all():
            if step_instance.status == Status.PENDING and step_instance.position == self.position:
                out += [step_instance]
        return out

    class Meta:
        verbose_name = 'کارمند دون‌پایه'


class Position(models.Model):
    name = models.CharField(max_length=40, verbose_name='نام')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'سمت'


class Process(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')
    first_step = models.ForeignKey(to='Step', related_name='+', verbose_name='گام اولیه',
                                   blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'فرایند'

    def clean(self):
        if self.first_step and self.first_step.process != self:
            raise ValidationError({'first_step': 'گام اولیه باید از گام‌های همین فرایند باشد'})


class Step(models.Model):
    process = models.ForeignKey(to=Process, related_name='steps', verbose_name='فرایند')
    name = models.CharField(max_length=100, verbose_name='نام')
    description = models.TextField(verbose_name='توضیحات')
    has_payment = models.BooleanField(verbose_name='امکان پرداخت')
    needs_clarification = models.BooleanField(verbose_name='امکان درخواست توضیح')
    pass_step = models.ForeignKey(to='Step', null=True, blank=True, related_name='+',
                                  verbose_name='گام بعدی در صورت موفقیت')
    fail_step = models.ForeignKey(to='Step', null=True, blank=True, related_name='+',
                                  verbose_name='گام بعدی در صورت شکست')
    position = models.ForeignKey(to=Position, related_name='steps', verbose_name='سمت مربوطه')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'گام'

    def clean(self):
        if self.pass_step and self.pass_step.process != self.process:
            raise ValidationError(
                {'pass_step': 'گام بعدی (در صورت موفقیت) باید از گام‌های همین فرایند باشد'})
        if self.fail_step and self.fail_step.process != self.process:
            raise ValidationError(
                {'fail_step': 'گام بعدی (در صورت شکست) باید از گام‌های همین فرایند باشد'})
