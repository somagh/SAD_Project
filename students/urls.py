from django.conf.urls import url

from students.views import StudentCreationView, StudentListView, StudentUpdatingView, StudentDeleteView

urlpatterns = [url(r'^student-new/', StudentCreationView.as_view(), name='student-create'),
               url(r'^student-list/', StudentListView.as_view(), name='student-list'),
               url(r'^student-update/(?P<pk>\d+)', StudentUpdatingView.as_view(), name='student-update'),
               url(r'^student-delete/(?P<pk>\d+)', StudentDeleteView.as_view(), name='student-delete'),
               url(r'^employee-new/', StudentCreationView.as_view(), name='employee-create'),
               url(r'^employee-list/', StudentListView.as_view(), name='employee-list'),
               url(r'^employee-update/(?P<pk>\d+)', StudentUpdatingView.as_view(), name='employee-update'),
               url(r'^employee-delete/(?P<pk>\d+)', StudentDeleteView.as_view(), name='employee-delete'),
               ]
