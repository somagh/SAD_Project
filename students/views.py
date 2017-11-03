from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from students.forms import StudentForm
from students.models import Student


class StudentCreationView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'create_student.html'
    success_url = '/students/list'


class StudentListView(ListView):
    model = Student
    template_name = 'list_student.html'


class StudentUpdatingView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'update_student.html'
    success_url = '/students/list'


class StudentDeleteView(DeleteView):
    model = Student
    success_url = '/students/list'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
