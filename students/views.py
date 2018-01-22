from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, FormView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from students.forms import StudentForm, EmployeeForm
from students.models import Student, Employee


class StudentCreateView(SuccessMessageMixin, FormView):
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


class StudentUpdateView(SuccessMessageMixin, FormView):
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

class EmployeeCreateView(SuccessMessageMixin, FormView):
    form_class = EmployeeForm
    template_name = 'create_employee.html'
    success_url = reverse_lazy('people:employee-list')
    success_message = "کارمند دون پایه جدید با موفقیت در سامانه ثبت شد"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class EmployeeUpdateView(SuccessMessageMixin, FormView):
    form_class = EmployeeForm
    template_name = 'update_employee.html'
    success_url = reverse_lazy('people:employee-list')
    success_message = "اطلاعات کارمند دون پایه در سامانه با موفقیت تغییر کرد"

    def get_object(self):
        return Employee.objects.get(pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        return {**{'instance': self.get_object()}, **super().get_form_kwargs()}

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class EmployeeListView(ListView):
    model = Employee
    template_name = 'list_employee.html'

class EmployeeDeleteView(SuccessMessageMixin, DeleteView):
    model = Employee
    success_url = reverse_lazy('people:employee-list')
    success_message = "کارمند دون پایه با موفقیت از سامانه حذف شد"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EmployeeDeleteView, self).delete(request, *args, **kwargs)

