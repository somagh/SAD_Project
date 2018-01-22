from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, FormView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from students.forms import StudentForm
from students.models import Student


class StudentCreationView(SuccessMessageMixin, FormView):
    form_class = StudentForm
    template_name = 'create_student.html'
    success_url = reverse_lazy('people:student-list')
    success_message = "دانشجوی جدید با موفقیت در سامانه ثبت شد"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class StudentListView(ListView):
    model = Student
    template_name = 'list_student.html'


class StudentUpdatingView(SuccessMessageMixin, FormView):
    form_class = StudentForm
    template_name = 'update_student.html'
    success_url = reverse_lazy('people:student-list')
    success_message = "اطلاعات دانشجو در سامانه با موفقیت تغییر کرد"

    def get_object(self):
        return Student.objects.get(pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        return {**{'instance': self.get_object()}, **super().get_form_kwargs()}

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class StudentDeleteView(SuccessMessageMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('people:student-list')
    success_message = "دانشجو با موفقیت از سامانه حذف شد"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(StudentDeleteView, self).delete(request, *args, **kwargs)
