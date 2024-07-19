from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    #def ready(self) -> None:
    #    from django.db.models.signals import post_save
    #    from . import signals
    #    post_save.connect(signals.new_user_activation_handler)