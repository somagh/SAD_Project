from django import forms
from django.contrib.auth.models import User

from students.models import Student


class UserCreationForm(forms.Form):
    first_name = forms.CharField(label='نام')
    last_name = forms.CharField(label='نام خانوادگی')
    password = forms.CharField(label='گذرواژه', widget=forms.PasswordInput)
    password_repeated = forms.CharField(label='تکرار گذرواژه', widget=forms.PasswordInput)
    email = forms.EmailField(label='رایانامه')

    def get_username(self):
        raise NotImplementedError

    def __init__(self, instance=None, **kwargs):
        super().__init__(**kwargs)
        self.instance = instance
        if instance:
            self.fields['first_name'].initial = instance.first_name
            self.fields['last_name'].initial = instance.last_name
            self.fields['email'].initial = instance.email
            self.fields['password'].required = False
            self.fields['password_repeated'].required = False

    def clean(self):
        data = super().clean()
        data['username'] = self.get_username()
        if not self.instance:
            if User.objects.filter(username=data['username']).exists():
                self.add_error(None, 'این نام کاربری قبلا گرفته شده است')
        if data['password'] != data['password_repeated']:
            self.add_error('password_repeated', 'گذرواژه‌های واردشده یکسان نیستند')
        return data

    def save(self):
        data = self.cleaned_data
        if not self.instance:
            user = User.objects.create_user(data['username'], email=data['email'], password=data['password'],
                                 first_name=data['first_name'], last_name=data['last_name'])
            return user
        else:
            self.instance.email = data['email']
            self.instance.first_name = data['first_name']
            self.instance.last_name = data['last_name']
            if data['password']:
                self.instance.set_password(data['password'])
            self.instance.save()
            return self.instance


class StudentForm(UserCreationForm):
    studentID = forms.CharField(label='شماره دانشجویی')

    def get_username(self):
        return 'student_' + self.data['studentID']

    def __init__(self, instance=None, **kwargs):
        self.instance = instance
        if instance:
            super().__init__(instance.user, **kwargs)
            self.fields['studentID'].initial = instance.studentID
            self.fields['studentID'].widget.attrs['readonly'] = True
        else:
            super().__init__(**kwargs)

    def clean(self):
        data = super().clean()
        if not self.instance:
            if Student.objects.filter(studentID=data['studentID']).exists():
                self.add_error('studentID', 'این شماره دانشجویی قبلا گرفته شده است')
        return data

    def save(self):
        user = super().save()
        if not self.instance:
            return Student.objects.create(user=user, studentID=self.cleaned_data['studentID'])
        else:
            self.instance.user = user
            self.instance.save()
            return self.instance