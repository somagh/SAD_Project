from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import RedirectView


class HomeView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            url = 'admin:student-list'
        elif hasattr(user, 'student'):
            url = ''
        elif hasattr(user, 'employee'):
            url = 'employee:show-responsibilities'
        return reverse(url)