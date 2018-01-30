from django.template.loader import render_to_string
from django.template.loader_tags import register

from student.models import Status


@register.simple_tag
def status_label(status):
    context = {}
    if status == Status.PENDING:
        context['pending'] = True
    elif status == Status.PASSED:
        context['passed'] = True
    elif status == Status.FAILED:
        context['failed'] = True
    elif status == Status.HAS_ERROR:
        context['has_error'] = True
    return render_to_string('status-label.html', context=context)
