from django.views.generic import ListView
from administrator.forms import StudentForm, EmployeeForm, PositionForm, ProcessForm, StepForm
from administrator.general_views import GeneralCreateView, GeneralUpdateView, GeneralDeleteView
from administrator.models import Student, Employee, Position, Step, Process


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


class StepCreateView(GeneralCreateView):
    form_class = StepForm


class StepUpdateView(GeneralUpdateView):
    form_class = StepForm


class StepListView(ListView):
    model = Step
    template_name = 'list_step.html'


class StepDeleteView(GeneralDeleteView):
    model = Step


class ProcessCreateView(GeneralCreateView):
    form_class = ProcessForm


class ProcessUpdateView(GeneralUpdateView):
    form_class = ProcessForm


class ProcessListView(ListView):
    model = Process
    template_name = 'list_process.html'


class ProcessDeleteView(GeneralDeleteView):
    model = Process