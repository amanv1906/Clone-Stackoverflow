from django.apps import AppConfig


class StackoverflowConfig(AppConfig):
    name = 'stackoverflow'

    def ready(self):
        import stackoverflow.signals # noqa
