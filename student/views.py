from django.shortcuts import redirect
from django.urls.base import reverse_lazy, reverse
from django.views.generic import FormView, TemplateView, DetailView
from django.views.generic.list import ListView

from SAD_Project.mixins import StudentRequiredMixin
from student.forms import ProcessInstanceForm
from student.models import PaymentAction, ClarificationAction


class ProcessInstanceCreateView(StudentRequiredMixin, FormView):
    form_class = ProcessInstanceForm
    template_name = 'start-process.html'
    success_url = reverse_lazy('student:home')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.student = self.request.student
        instance.save()
        return super().form_valid(form)


class HomeView(StudentRequiredMixin, TemplateView):
    template_name = 'student-home.html'


class ShowStepsView(StudentRequiredMixin, ListView):
    template_name = 'show-steps.html'
    context_object_name = 'step_instances'

    def get_queryset(self):
        return self.request.student.process_instances.get(pk=int(self.kwargs['process_instance_pk'])).step_instances.all()


class ShowActionsView(StudentRequiredMixin, ListView):
    template_name = 'show-actions.html'
    context_object_name = 'actions'

    def get_queryset(self):
        return self.request.student.process_instances.get(
            pk=int(self.kwargs['process_instance_pk'])).step_instances.get(
            pk=int(self.kwargs['pk'])).actions.all()


class PaymentWrapper:
    def __init__(self, action):
        self.action = action

    def go_to_payment(self):
        pass

    def from_payment(self, pursuit):
        PaymentAction.objects.create(step_instance=self.action.step_instance, pursuit=pursuit)
        return redirect(reverse('student:steps', args=[self.action.step_instance.process_instance.pk]))


class FakePaymentWrapper(PaymentWrapper):
    def go_to_payment(self):
        return self.from_payment('FAKE ONE')


class PaymentActionView(StudentRequiredMixin, DetailView):
    template_name = 'payment-action.html'
    context_object_name = 'action'

    def get_object(self, queryset=None):
        return self.request.student.process_instances.get(
            pk=int(self.kwargs['process_instance_pk'])).step_instances.get(
            pk=int(self.kwargs['pk'])).actions.last()

    def post(self, request, *args, **kwargs):
        action = self.get_object()
        if action.step_instance.check_action_validation(None, PaymentAction):
            return FakePaymentWrapper(self.get_object()).go_to_payment()


class ClarificationActionView(StudentRequiredMixin, DetailView):
    template_name = 'clarification-action.html'
    context_object_name = 'action'

    def get_object(self, queryset=None):
        return self.request.student.process_instances.get(
            pk=int(self.kwargs['process_instance_pk'])).step_instances.get(
            pk=int(self.kwargs['pk'])).actions.last()

    def post(self, request, *args, **kwargs):
        action = self.get_object()
        if action.step_instance.check_action_validation(None, ClarificationAction):
            ClarificationAction.objects.create(response=request.POST['response'],
                                               step_instance=action.step_instance)
        return redirect(reverse('student:steps', args=[action.step_instance.process_instance.pk]))
