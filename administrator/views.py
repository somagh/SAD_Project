from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, FormView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView
from administrator.forms import StudentForm, EmployeeForm
from administrator.models import Student, Employee, Position


class StudentCreateView(SuccessMessageMixin, FormView):
    form_class = StudentForm
    template_name = 'create_update.html'
    success_url = reverse_lazy('admin:student-list')
    success_message = "دانشجوی جدید با موفقیت در سامانه ثبت شد"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'اضافه کردن'
        context['model_name'] = 'دانشجو'
        context['back_url'] = self.success_url
        return context


class StudentListView(ListView):
    model = Student
    template_name = 'list_student.html'


class StudentUpdateView(SuccessMessageMixin, FormView):
    form_class = StudentForm
    template_name = 'create_update.html'
    success_url = reverse_lazy('admin:student-list')
    success_message = "اطلاعات دانشجو در سامانه با موفقیت تغییر کرد"

    def get_object(self):
        return Student.objects.get(pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        return {**{'student': self.get_object()}, **super().get_form_kwargs()}

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'ویرایش'
        context['model_name'] = 'دانشجو'
        context['back_url'] = self.success_url
        return context


class StudentDeleteView(SuccessMessageMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('admin:student-list')
    success_message = "دانشجو با موفقیت از سامانه حذف شد"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class EmployeeCreateView(SuccessMessageMixin, FormView):
    form_class = EmployeeForm
    template_name = 'create_update.html'
    success_url = reverse_lazy('admin:employee-list')
    success_message = "کارمند دون پایه جدید با موفقیت در سامانه ثبت شد"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'اضافه کردن'
        context['model_name'] = 'کارمند دون‌پایه'
        context['back_url'] = self.success_url
        return context


class EmployeeUpdateView(SuccessMessageMixin, FormView):
    form_class = EmployeeForm
    template_name = 'create_update.html'
    success_url = reverse_lazy('admin:employee-list')
    success_message = "اطلاعات کارمند دون پایه در سامانه با موفقیت تغییر کرد"

    def get_object(self):
        return Employee.objects.get(pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        return {**{'employee': self.get_object()}, **super().get_form_kwargs()}

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'ویرایش'
        context['model_name'] = 'کارمند دون‌پایه'
        context['back_url'] = self.success_url
        return context


class EmployeeListView(ListView):
    model = Employee
    template_name = 'list_employee.html'


class EmployeeDeleteView(SuccessMessageMixin, DeleteView):
    model = Employee
    success_url = reverse_lazy('admin:employee-list')
    success_message = "کارمند دون پایه با موفقیت از سامانه حذف شد"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class PositionCreateView(SuccessMessageMixin, CreateView):
    model = Position
    fields = '__all__'
    template_name = 'create_update.html'
    success_url = reverse_lazy('admin:position-list')
    success_message = "سمت جدید با موفقیت در سامانه ثبت شد"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'اضافه کردن'
        context['model_name'] = 'سمت'
        context['back_url'] = self.success_url
        return context


class PositionUpdateView(SuccessMessageMixin, UpdateView):
    model = Position
    fields = '__all__'
    template_name = 'create_update.html'
    success_url = reverse_lazy('admin:position-list')
    success_message = "اطلاعات سمت در سامانه با موفقیت تغییر کرد"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'ویرایش'
        context['model_name'] = 'سمت'
        context['back_url'] = self.success_url
        return context


class PositionListView(ListView):
    model = Position
    template_name = 'list_position.html'


class PositionDeleteView(SuccessMessageMixin, DeleteView):
    model = Position
    success_url = reverse_lazy('admin:position-list')
    success_message = "سمت با موفقیت از سامانه حذف شد"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
