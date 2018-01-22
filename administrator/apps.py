from django.apps import AppConfig
from django.db.models.signals import pre_save


class AdminstratorConfig(AppConfig):
    name = 'administrator'


def validate_model(self, instance, raw=False, **kwargs):
    if not raw:
        instance.full_clean()


pre_save.connect(validate_model, dispatch='validate_model')