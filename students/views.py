from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from students.forms import StudentForm
from students.models import Student


class StudentCreationView(SuccessMessageMixin,CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'create_student.html'
    success_url = '/students/list'
    success_message = "دانشجوی جدید با موفقیت در سامانه ثبت شد"



class StudentListView(ListView):
    model = Student
    template_name = 'list_student.html'


class StudentUpdatingView(SuccessMessageMixin,UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'update_student.html'
    success_url = '/students/list'
    success_message = "اطلاعات دانشجو در سامانه با موفقیت تغییر کرد"


class StudentDeleteView(SuccessMessageMixin,DeleteView):
    model = Student
    success_url = '/students/list'
    success_message = "دانشجو با موفقیت از سامانه حذف شد"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(StudentDeleteView, self).delete(request, *args, **kwargs)
