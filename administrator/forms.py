from django import forms
from django.contrib.auth.models import User
from docutils.utils.math.math2html import Position

from administrator.models import Student, Employee, Position


class UserCreationForm(forms.Form):
    first_name = forms.CharField(label='نام')
    last_name = forms.CharField(label='نام خانوادگی')
    password = forms.CharField(label='گذرواژه', widget=forms.PasswordInput)
    password_repeated = forms.CharField(label='تکرار گذرواژه', widget=forms.PasswordInput)
    email = forms.EmailField(label='رایانامه')

    def get_username(self):
        raise NotImplementedError

    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)
        self.user = user
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['password'].required = False
            self.fields['password_repeated'].required = False

    def clean(self):
        data = super().clean()
        data['username'] = self.get_username()
        if not self.user:
            if User.objects.filter(username=data['username']).exists():
                self.add_error(None, 'این نام کاربری قبلا گرفته شده است')
        if data['password'] != data['password_repeated']:
            self.add_error('password_repeated', 'گذرواژه‌های واردشده یکسان نیستند')
        return data

    def save(self):
        data = self.cleaned_data
        if not self.user:
            user = User.objects.create_user(data['username'], email=data['email'],
                                            password=data['password'],
                                            first_name=data['first_name'],
                                            last_name=data['last_name'])
            return user
        else:
            self.user.email = data['email']
            self.user.first_name = data['first_name']
            self.user.last_name = data['last_name']
            if data['password']:
                self.user.set_password(data['password'])
            self.user.save()
            return self.user


class StudentForm(UserCreationForm):
    studentID = forms.CharField(label='شماره دانشجویی')

    def get_username(self):
        return 'student_' + self.data['studentID']

    def __init__(self, student=None, **kwargs):
        self.student = student
        if student:
            super().__init__(student.user, **kwargs)
            self.fields['studentID'].initial = student.studentID
            self.fields['studentID'].widget.attrs['readonly'] = True
        else:
            super().__init__(**kwargs)

    def clean(self):
        data = super().clean()
        if not self.student:
            if Student.objects.filter(studentID=data['studentID']).exists():
                self.add_error('studentID', 'این شماره دانشجویی قبلا گرفته شده است')
        return data

    def save(self):
        user = super().save()
        if not self.student:
            return Student.objects.create(user=user, studentID=self.cleaned_data['studentID'])
        else:
            self.student.user = user
            self.student.save()
            return self.student


class EmployeeForm(UserCreationForm):
    position = forms.ModelChoiceField(queryset=Position.objects.all(), label="سمت")

    def get_username(self):
        return 'employee_' + str(Employee.objects.last().pk + 1 if Employee.objects.last() else 1)

    def __init__(self, employee=None, **kwargs):
        self.employee = employee
        if employee:
            super().__init__(employee.user, **kwargs)
            self.fields['position'].initial = employee.position
        else:
            super().__init__(**kwargs)

    def save(self):
        user = super().save()
        if not self.employee:
            return Employee.objects.create(user=user, position=self.cleaned_data['position'])
        else:
            self.employee.user = user
            self.employee.position = self.cleaned_data['position']
            self.employee.save()
            return self.employee
