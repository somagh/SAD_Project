from django.views.generic import ListView
from administrator.forms import StudentForm, EmployeeForm, PositionForm, ProcessForm, StepForm
from administrator.general_views import GeneralCreateView, GeneralUpdateView, GeneralDeleteView, GeneralListView
from administrator.models import Student, Employee, Position, Step, Process


class StudentCreateView(GeneralCreateView):
    form_class = StudentForm


class StudentListView(GeneralListView):
    model = Student


class StudentUpdateView(GeneralUpdateView):
    form_class = StudentForm


class StudentDeleteView(GeneralDeleteView):
    model = Student


class EmployeeCreateView(GeneralCreateView):
    form_class = EmployeeForm


class EmployeeUpdateView(GeneralUpdateView):
    form_class = EmployeeForm


class EmployeeListView(GeneralListView):
    model = Employee


class EmployeeDeleteView(GeneralDeleteView):
    model = Employee


class PositionCreateView(GeneralCreateView):
    form_class = PositionForm


class PositionUpdateView(GeneralUpdateView):
    form_class = PositionForm


class PositionListView(GeneralListView):
    model = Position


class PositionDeleteView(GeneralDeleteView):
    model = Position


class StepCreateView(GeneralCreateView):
    form_class = StepForm


class StepUpdateView(GeneralUpdateView):
    form_class = StepForm


class StepListView(GeneralListView):
    model = Step


class StepDeleteView(GeneralDeleteView):
    model = Step


class ProcessCreateView(GeneralCreateView):
    form_class = ProcessForm


class ProcessUpdateView(GeneralUpdateView):
    form_class = ProcessForm


class ProcessListView(GeneralListView):
    model = Process


class ProcessDeleteView(GeneralDeleteView):
    model = Process