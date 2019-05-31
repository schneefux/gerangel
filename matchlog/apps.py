from django.apps import AppConfig


class MatchlogConfig(AppConfig):
    name = 'matchlog'

    def ready(self):
        import matchlog.signals
