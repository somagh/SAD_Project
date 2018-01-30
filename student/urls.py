from django.conf.urls import url, include

from student.views import ProcessInstanceCreateView, HomeView, ShowStepsView, ShowActionsView, \
    PaymentActionView, ClarificationActionView

step_instance_urlpatterns = [
    url(r'^$', ShowActionsView.as_view(), name='actions'),
    url(r'^payment/$', PaymentActionView.as_view(), name='payment-action'),
    url(r'^clarification/$', ClarificationActionView.as_view(), name='clarification-action'),
]

urlpatterns = [
    url(r'^home/', HomeView.as_view(), name='home'),
    url(r'^start-process/', ProcessInstanceCreateView.as_view(), name='start-process'),
    url(r'^(?P<process_instance_pk>\d+)/steps/$', ShowStepsView.as_view(), name='steps'),
    url(r'^(?P<process_instance_pk>\d+)/steps/(?P<pk>\d+)/', include(step_instance_urlpatterns)),
]
