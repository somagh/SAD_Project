from django.conf.urls import url

from students.views import StudentCreationView, StudentListView, StudentUpdatingView, StudentDeleteView

urlpatterns = [url(r'^new/', StudentCreationView.as_view(), name='create'),
               url(r'^list/', StudentListView.as_view(), name='list'),
               url(r'^update/(?P<pk>\d+)', StudentUpdatingView.as_view(), name='update'),
               url(r'^delete/(?P<pk>\d+)', StudentDeleteView.as_view(), name='delete'),
               ]
