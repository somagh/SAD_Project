from django.views.generic import FormView, DetailView

from SAD_Project.mixins import StudentRequiredMixin
from student.forms import ProcessInstanceForm


class ProcessInstanceCreateView(StudentRequiredMixin, FormView):
    form_class = ProcessInstanceForm
    template_name = 'start-process.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.student = self.request.student
        instance.save()
        return super().form_valid(form)
