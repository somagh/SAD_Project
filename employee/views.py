from django.shortcuts import redirect
from django.views.generic import ListView, FormView
from django.views.generic.base import TemplateView
from django.views import View
from django.views.generic import ListView
from django.views.generic import RedirectView
from django.views.generic.detail import DetailView

from SAD_Project.mixins import EmployeeRequiredMixin
from student.models import StepInstance, Status, PaymentRecommit, ClarificationRecommit
from student.models import StepInstance, Status, PassFailAction


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
    context_object_name = 'step_instance'
    template_name = 'recommit-step-instance.html'

    def get_object(self, queryset=None):
        step_instance = super().get_object(queryset=queryset)
        if step_instance.position != self.request.employee.position \
                or step_instance.status != Status.PENDING:
            raise PermissionError
        return step_instance

    def post(self, request, *args, **kwargs):
        step_instance = self.get_object()
        action_class = PaymentRecommit if request.POST[
                                              'recommit_type'] == 'payment' else ClarificationRecommit
        if step_instance.check_action_validation(request.employee, action_class):
            if action_class == PaymentRecommit:
                PaymentRecommit.objects.create(step_instance=step_instance,
                                               employee=request.employee,
                                               price=int(request.POST['price']),
                                               concern=request.POST['concern'])
            else:
                ClarificationRecommit.objects.create(step_instance=step_instance,
                                                     employee=request.employee,
                                                     message=request.POST['message'])
        return redirect('employee:show-responsibilities')


class PassFailActionCreateView(EmployeeRequiredMixin, DetailView):
    model = StepInstance
    context_object_name = 'step_instance'

    def get(self, request, *args, **kwargs):
        step_instance=self.get_object()
        if step_instance.check_action_validation(request.employee,PassFailAction):
            PassFailAction.objects.create(step_instance=step_instance,employee=request.employee,status=Status.PASSED if request.GET['type']=='accept' else Status.FAILED)
        return redirect('employee:show-responsibilities')


class EmployeeReportView(EmployeeRequiredMixin, TemplateView):
    template_name = 'employee-report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        payment_recommits = PaymentRecommit.objects.filter(employee=self.request.employee)
        clarification_recommits = ClarificationRecommit.objects.filter(employee=self.request.employee)
        pass_fail_actions = PassFailAction.objects.filter(employee=self.request.employee)
        context['action_set'] = [
            {'title': 'خطا‌های پرداختی', 'actions': payment_recommits},
            {'title': 'خطاهای نیازمند توضیح', 'actions': clarification_recommits},
            {'title': 'تاریخچه‌ی رد یا تایید', 'actions': pass_fail_actions},
        ]
        return context