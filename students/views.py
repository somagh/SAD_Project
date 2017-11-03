from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic import ListView

from students.forms import StudentCreationForm
from students.models import Student


class StudentCreationView(CreateView):
    model=Student
    form_class = StudentCreationForm
    template_name = 'create_student.html'
    success_url = '/students/list'

class StudentListView(ListView):
    model=Student
    template_name = 'list_student.html'