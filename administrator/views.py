from django.views.generic import ListView
from administrator.forms import StudentForm, EmployeeForm, PositionForm
from administrator.general_views import GeneralCreateView, GeneralUpdateView, GeneralDeleteView
from administrator.models import Student, Employee, Position, Step


class StudentCreateView(GeneralCreateView):
    form_class = StudentForm


class StudentListView(ListView):
    model = Student
    template_name = 'list_student.html'


class StudentUpdateView(GeneralUpdateView):
    form_class = StudentForm


class StudentDeleteView(GeneralDeleteView):
    model = Student


class EmployeeCreateView(GeneralCreateView):
    model = Employee
    form_class = EmployeeForm


class EmployeeUpdateView(GeneralUpdateView):
    form_class = EmployeeForm


class EmployeeListView(ListView):
    model = Employee
    template_name = 'list_employee.html'


class EmployeeDeleteView(GeneralDeleteView):
    model = Employee


class PositionCreateView(GeneralCreateView):
    form_class = PositionForm


class PositionUpdateView(GeneralUpdateView):
    form_class = PositionForm


class PositionListView(ListView):
    model = Position
    template_name = 'list_position.html'


class PositionDeleteView(GeneralDeleteView):
    model = Position
