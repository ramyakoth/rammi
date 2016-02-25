from __future__ import unicode_literals
from django.apps import AppConfig


class FalconAppConfig(AppConfig):
    name = 'falcon_app'

    def ready(self):
        pass
