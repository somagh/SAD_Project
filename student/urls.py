from django.conf.urls import url

from student.views import ProcessInstanceCreateView, HomeView, ShowStepsView, ShowActionsView

urlpatterns = [
    url(r'^home/', HomeView.as_view(), name='home'),
    url(r'^start-process/', ProcessInstanceCreateView.as_view(), name='start-process'),
    url(r'^(?P<process_instance_pk>\d+)/steps/$', ShowStepsView.as_view(), name='steps'),
    url(r'^(?P<process_instance_pk>\d+)/steps/(?P<pk>\d+)', ShowActionsView.as_view(), name='actions'),
]
