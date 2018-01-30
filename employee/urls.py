from django.conf.urls import url

from employee.views import ShowResponsibilitiesView, CheckStepInstanceView, RecommitStepInstanceView, \
    PassFailActionCreateView, EmployeeReportView

urlpatterns = [
    url(r'^show-responsibilities/', ShowResponsibilitiesView.as_view(), name='show-responsibilities'),
    url(r'^check/(?P<pk>\d+)', CheckStepInstanceView.as_view(), name='check-step-instance'),
    url(r'^recommit/(?P<pk>\d+)', RecommitStepInstanceView.as_view(), name='recommit-step-instance'),
    url(r'^passfail/(?P<pk>\d+)',PassFailActionCreateView.as_view(),name='passfail-step-instance'),
    url(r'^report/',EmployeeReportView.as_view(),name='report'),
    ]
