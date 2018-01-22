from django.core.exceptions import ValidationError
from django.db import models
from enumfields.enums import Enum
from enumfields.fields import EnumField
from polymorphic.models import PolymorphicModel

from administrator.models import Step, Process, Student, Employee


class Status(Enum):
    PENDING = 'pending'
    FAILED = 'failed'
    PASSED = 'passed'
    HAS_ERROR = 'has_error'


class ProcessInstance(models.Model):
    process = models.ForeignKey(to=Process, verbose_name='فرایند')
    student = models.ForeignKey(to=Student)

    def clean(self):
        if not self.process.first_step:
            raise ValidationError('Process has no first step')

    def save(self, **kwargs):
        if not self.pk:
            super().save(**kwargs)
            StepInstance.objects.create(process_instance=self, step=self.process.first_step)
        else:
            super().save(**kwargs)


class StepInstance(models.Model):
    process_instance = models.ForeignKey(to=ProcessInstance, related_name='step_instances')
    step = models.ForeignKey(to=Step)
    start_date = models.DateField(auto_now_add=True)

    @property
    def process(self):
        return self.process_instance.process

    @property
    def student(self):
        return self.process_instance.student

    @property
    def last_action(self):
        return self.actions.last()

    @property
    def end_date(self):
        action = self.last_action
        if isinstance(action, PassFailAction):
            return action.date

    @property
    def position(self):
        return self.step.position

    @property
    def status(self):
        action = self.last_action
        if action:
            return action.status
        else:
            return Status.PENDING

    def clean(self):
        if self.process_instance.process != self.step.process:
            raise ValidationError('process_instance.process should be same as step.process')


class Action(PolymorphicModel):
    step_instance = models.ForeignKey(to=StepInstance, related_name='actions')
    date = models.DateField(auto_now_add=True)

    @property
    def is_student_action(self):
        return hasattr(self, 'employee')

    class Meta:
        ordering = ('date',)


class PassFailAction(Action):
    employee = models.ForeignKey(to=Employee)
    status = EnumField(Status)

    def clean(self):
        if self.status != Status.FAILED and self.status != Status.PASSED:
            raise ValidationError({'status': 'Invalid Status for PassFailAction, '
                                             'Choices are: FAILED and PASSED'})


class PaymentRecommit(Action):
    employee = models.ForeignKey(to=Employee)
    price = models.IntegerField()
    concern = models.TextField()

    @property
    def status(self):
        return Status.HAS_ERROR


class ClarificationRecommit(Action):
    employee = models.ForeignKey(to=Employee)
    message = models.TextField()

    @property
    def status(self):
        return Status.HAS_ERROR


class PaymentAction(Action):
    pursuit = models.CharField(max_length=100)

    @property
    def status(self):
        return Status.PENDING


class ClarificationAction(Action):
    response = models.TextField()

    @property
    def status(self):
        return Status.PENDING
