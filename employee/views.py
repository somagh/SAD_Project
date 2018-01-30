from django.views.generic import ListView, FormView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from SAD_Project.mixins import EmployeeRequiredMixin
from student.models import StepInstance, Status


class ShowResponsibilitiesView(EmployeeRequiredMixin, ListView):
    template_name = 'show-responsibilities.html'
    context_object_name = 'step_instances'

    def get_queryset(self):
        return self.request.employee.get_related_step_instances()


class CheckStepInstanceView(EmployeeRequiredMixin, DetailView):
    model = StepInstance
    template_name = 'check-step-instance.html'
    context_object_name = 'step_instance'

    def get_object(self, queryset=None):
        step_instance = super().get_object(queryset=queryset)
        if step_instance.position != self.request.employee.position \
                or step_instance.status != Status.PENDING:
            raise PermissionError
        return step_instance


class RecommitStepInstanceView(EmployeeRequiredMixin, DetailView):
    model = StepInstance

    def get_object(self, queryset=None):
        step_instance = super().get_object(queryset=queryset)
        if step_instance.position != self.request.employee.position \
                or step_instance.status != Status.PENDING:
            raise PermissionError
        return step_instance

    def post(self, request, *args, **kwargs):
        step_instance = self.get_object()

