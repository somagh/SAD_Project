from django.conf.urls import url

from employee.views import ShowResponsibilitiesView, CheckStepInstanceView

urlpatterns = [
    url(r'^show-responsibilities/', ShowResponsibilitiesView.as_view(), name='show-responsibilities'),
    url(r'^check/(?P<pk>\d+)', CheckStepInstanceView.as_view(), name='check-step-instance'),
        ]
