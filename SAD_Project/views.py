from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import RedirectView


class HomeView(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('admin:student-list')