from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=50,verbose_name='نام')
    last_name = models.CharField(max_length=50,verbose_name='نام خانوادگی')
    birth_date = models.DateField(verbose_name='تاریخ تولد')
    national_code = models.CharField(max_length=10,verbose_name='شماره شناسنامه',unique=True)


