from django.conf.urls import url

from administrator.views import StudentListView,  StudentDeleteView, \
    StudentUpdateView, EmployeeCreateView, EmployeeListView, StudentCreateView, EmployeeUpdateView, EmployeeDeleteView, \
    PositionCreateView, PositionListView, PositionUpdateView, PositionDeleteView, ProcessCreateView, ProcessListView, \
    ProcessUpdateView, ProcessDeleteView, StepCreateView, StepListView, StepUpdateView, StepDeleteView

urlpatterns = [url(r'^student-new/', StudentCreateView.as_view(), name='student-create'),
               url(r'^student-list/', StudentListView.as_view(), name='student-list'),
               url(r'^student-update/(?P<pk>\d+)', StudentUpdateView.as_view(), name='student-update'),
               url(r'^student-delete/(?P<pk>\d+)', StudentDeleteView.as_view(), name='student-delete'),
               url(r'^employee-new/', EmployeeCreateView.as_view(), name='employee-create'),
               url(r'^employee-list/', EmployeeListView.as_view(), name='employee-list'),
               url(r'^employee-update/(?P<pk>\d+)', EmployeeUpdateView.as_view(), name='employee-update'),
               url(r'^employee-delete/(?P<pk>\d+)', EmployeeDeleteView.as_view(), name='employee-delete'),
               url(r'^position-new/', PositionCreateView.as_view(), name='position-create'),
               url(r'^position-list/', PositionListView.as_view(), name='position-list'),
               url(r'^position-update/(?P<pk>\d+)', PositionUpdateView.as_view(), name='position-update'),
               url(r'^position-delete/(?P<pk>\d+)', PositionDeleteView.as_view(), name='position-delete'),
               url(r'^process-new/', ProcessCreateView.as_view(), name='process-create'),
               url(r'^process-list/', ProcessListView.as_view(), name='process-list'),
               url(r'^process-update/(?P<pk>\d+)', ProcessUpdateView.as_view(), name='process-update'),
               url(r'^process-delete/(?P<pk>\d+)', ProcessDeleteView.as_view(), name='process-delete'),
               url(r'^step-new/', StepCreateView.as_view(), name='step-create'),
               url(r'^step-list/', StepListView.as_view(), name='step-list'),
               url(r'^step-update/(?P<pk>\d+)', StepUpdateView.as_view(), name='step-update'),
               url(r'^step-delete/(?P<pk>\d+)', StepDeleteView.as_view(), name='step-delete'),
               ]
