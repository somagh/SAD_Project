from django.urls.base import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from SAD_Project.mixins import StudentRequiredMixin
from student.forms import ProcessInstanceForm
from student.models import StepInstance


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