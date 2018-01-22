from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import FormView, DeleteView


class GeneralCreateView(SuccessMessageMixin, FormView):
    template_name = 'create_update.html'
    form_class = None

    @property
    def model(self):
        return self.form_class.Meta.model

    def get_success_message(self, cleaned_data):
        return self.model._meta.verbose_name + ' جدید با موفقیت در سامانه اضافه شد.'

    def get_success_url(self):
        return reverse('admin:{}-list'.format(self.model.__name__.lower()))

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'اضافه کردن'
        context['model_name'] = self.model._meta.verbose_name
        context['back_url'] = self.get_success_url()
        return context

class GeneralUpdateView(GeneralCreateView):

    def get_object(self):
        return self.model.objects.get(pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        return {**{'instance': self.get_object()}, **super().get_form_kwargs()}


    def get_success_message(self, cleaned_data):
        return 'اطلاعات '+ self.model._meta.verbose_name + ' با موفقیت تغییر کرد.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'ویرایش'
        return context


class GeneralDeleteView(SuccessMessageMixin, DeleteView):
    model = None

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('admin:{}-list'.format(self.model.__name__.lower()))

    def delete(self, request, *args, **kwargs):
        success_message = self.model._meta.verbose_name + ' با موفقیت از سامانه حذف شد.'
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)
