from django.conf.urls import url

from student.views import ProcessInstanceCreateView

urlpatterns = [
    url(r'^start-process/', ProcessInstanceCreateView.as_view(), name='start-process'),
    ]
