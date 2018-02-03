from django.core.exceptions import ValidationError
from django.db import models
from django.db import transaction
from enumfields.enums import Enum
from enumfields.fields import EnumField
from polymorphic.models import PolymorphicModel

from administrator.models import Step, Process, Student, Employee, PaymentTransaction


class Status(Enum):
    PENDING = 'pending'
    FAILED = 'failed'
    PASSED = 'passed'
    HAS_ERROR = 'has_error'


class ProcessInstance(models.Model):
    process = models.ForeignKey(to=Process, verbose_name='فرایند')
    student = models.ForeignKey(to=Student, related_name='process_instances')

    @property
    def status(self):
        return self.step_instances.last().status

    @property
    def start_date(self):
        return self.step_instances.first().start_date

    @property
    def name(self):
        return self.process.name

    def clean(self):
        if not self.process.first_step:
            raise ValidationError('Process has no first step')

    def get_payment_transactions(self):
        transactions = []
        for step_instance in self.step_instances.all():
            transactions += step_instance.get_payment_transactions()
        return transactions

    def save(self, **kwargs):
        if not self.pk:
            super().save(**kwargs)
            StepInstance.objects.create(process_instance=self, step=self.process.first_step)
        else:
            super().save(**kwargs)

    class Meta:
        ordering = ('-pk',)


class StepInstance(models.Model):
    process_instance = models.ForeignKey(to=ProcessInstance, related_name='step_instances')
    step = models.ForeignKey(to=Step)
    start_date = models.DateTimeField(auto_now_add=True)

    @property
    def name(self):
        return self.step.name

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

    @property
    def has_payment_recommit(self):
        return isinstance(self.last_action, PaymentRecommit)

    @property
    def has_clarification_recommit(self):
        return isinstance(self.last_action, ClarificationRecommit)

    def get_payment_transactions(self):
        transactions = []
        actions = self.actions.all()
        for i in range(len(actions) - 1):
            next = actions[i+1]
            prev = actions[i]
            if next.is_paid_payment_action:
                transactions.append(PaymentTransaction(price=prev.price, concern=prev.concern,
                                                       pursuit=next.pursuit, date=next.date))
        return transactions

    def check_action_validation(self, employee, action_class):
        if employee:
            if self.position != employee.position or self.status != Status.PENDING:
                return False
        else:
            if self.status != Status.HAS_ERROR:
                return False
        return action_class.is_valid(self)

    def clean(self):
        if self.process_instance.process != self.step.process:
            raise ValidationError('process_instance.process should be same as step.process')

    class Meta:
        ordering = ('start_date',)


class Action(PolymorphicModel):
    step_instance = models.ForeignKey(to=StepInstance, related_name='actions')
    date = models.DateTimeField(auto_now_add=True)

    @property
    def is_paid_payment_action(self):
        return False

    @property
    def is_student_action(self):
        return not hasattr(self, 'employee')

    @property
    def details(self):
        return '--'

    class Meta:
        ordering = ('date',)

    @staticmethod
    def is_valid(step_instance):
        return False

    def save(self,**kwargs):
        super().save()
        self.notify()

    def notify(self):
        pass



class PassFailAction(Action):
    employee = models.ForeignKey(to=Employee)
    status = EnumField(Status)

    def clean(self):
        if self.status != Status.FAILED and self.status != Status.PASSED:
            raise ValidationError({'status': 'Invalid Status for PassFailAction, '
                                             'Choices are: FAILED and PASSED'})

    @staticmethod
    def is_valid(step_instance):
        return True

    def save(self, **kwargs):
        if not self.pk:
            with transaction.atomic():
                super().save(**kwargs)
                if self.status==Status.PASSED and self.step_instance.step.pass_step:
                    StepInstance.objects.create(process_instance=self.step_instance.process_instance, step=self.step_instance.step.pass_step)
                if self.status==Status.FAILED and self.step_instance.step.fail_step:
                    StepInstance.objects.create(process_instance=self.step_instance.process_instance, step=self.step_instance.step.fail_step)
        else:
            super().save(**kwargs)

    def notify(self):
        if self.status==Status.PASSED:
            if self.step_instance.step.pass_step is not None:
                subject='پذیرش گام'
                message='سلام {}،\nدر فرایند {}، گام {} شما  با موفقیت پذیرفته شد و حال به گام {} وارد شده اید.'.format(self.step_instance.student.full_name,self.step_instance.process_instance.name,self.step_instance.name,self.step_instance.step.pass_step.name)
            else:
                subject='پایان موفقیت آمیز فرایند'
                message='سلام {}،\nبا پذیرش گام {}، فرایند {} با موفقیت به پایان رسید.'.format(self.step_instance.student.full_name,self.step_instance.name,self.step_instance.process_instance.name)
        else:
            if self.step_instance.step.fail_step is not None:
                subject = 'رد گام'
                message = 'سلام {}،\nدر فرایند {}، متاسفانه گام {} شما رد شد و حال به گام {} وارد شده اید.'.format(self.step_instance.student.full_name,self.step_instance.process_instance.name,self.step_instance.name,self.step_instance.step.fail_step.name)
            else:
                subject = 'پایان ناموفق فرایند'
                message = 'سلام {}،\nبا رد گام {}، فرایند {} بدون موفقیت به پایان رسید.'.format(self.step_instance.student.full_name,self.step_instance.name,self.step_instance.process_instance.name)
        self.step_instance.student.notify(subject,message)


class PaymentRecommit(Action):
    employee = models.ForeignKey(to=Employee)
    price = models.IntegerField()
    concern = models.TextField()

    @property
    def details(self):
        price_label = 'مبلغ'
        concern_label = 'باید بابت'
        end_label = 'پرداخت شود.'
        return '{} {} {} {} {}'.format(price_label, self.price, concern_label, self.concern, end_label)

    @property
    def status(self):
        return Status.HAS_ERROR

    @staticmethod
    def is_valid(step_instance):
        return step_instance.step.has_payment

    def notify(self):
        subject='نیاز به پرداخت وجه'
        message='سلام {}،\nدر گام {} فرایند {}، باید مبلغ {} تومان بابت {} پرداخت کنید.'.format(self.step_instance.student.full_name,self.step_instance.name,self.step_instance.process_instance.name,self.price,self.concern)
        self.step_instance.student.notify(subject,message)


class ClarificationRecommit(Action):
    employee = models.ForeignKey(to=Employee)
    message = models.TextField()

    @property
    def details(self):
        label = 'خطایی با این مضمون به وجود آمد: '
        return '{} {}'.format(label, self.message)

    @property
    def status(self):
        return Status.HAS_ERROR

    @staticmethod
    def is_valid(step_instance):
        return step_instance.step.needs_clarification

    def notify(self):
        subject='نیاز به ادای توضیحات'
        message='سلام {}،\nدر گام {} فرایند {}، خطایی با مضمون {} به وجود آمده است.'.format(self.step_instance.student.full_name,self.step_instance.name,self.step_instance.process_instance.name,self.message)
        self.step_instance.student.notify(subject,message)


class PaymentAction(Action):
    pursuit = models.CharField(max_length=100)

    @property
    def is_paid_payment_action(self):
        return True

    @property
    def details(self):
        label = 'مبلغ مدنظر پرداخت شد؛ کد رهگیری: '
        return '{} {}'.format(label, self.pursuit)

    @property
    def status(self):
        return Status.PENDING

    @staticmethod
    def is_valid(step_instance):
        return isinstance(step_instance.last_action, PaymentRecommit)


class ClarificationAction(Action):
    response = models.TextField()

    @property
    def details(self):
        label = 'مستندات ارائه‌شده توسط دانشجو: '
        return '{} {}'.format(label, self.response)

    @property
    def status(self):
        return Status.PENDING

    @staticmethod
    def is_valid(step_instance):
        return isinstance(step_instance.last_action, ClarificationRecommit)
