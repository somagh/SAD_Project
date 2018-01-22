from django import forms

from student.models import ProcessInstance


class ProcessInstanceForm(forms.ModelForm):
    class Meta:
        model = ProcessInstance
        fields = ('process',)
