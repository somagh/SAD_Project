from django.conf.urls import url

from students.views import StudentCreationView, StudentListView

urlpatterns=[url(r'^new/', StudentCreationView.as_view(),name='create'),
             url(r'^list/', StudentListView.as_view(), name='list'),
             ]