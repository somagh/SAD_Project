from django.contrib.auth.mixins import AccessMixin


class AdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class StudentRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'student'):
            return self.handle_no_permission()
        request.student = request.user.student
        return super().dispatch(request, *args, **kwargs)


class EmployeeRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'employee'):
            return self.handle_no_permission()
        request.employee = request.user.employee
        return super().dispatch(request, *args, **kwargs)
