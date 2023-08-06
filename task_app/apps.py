from django.apps import AppConfig


class TaskHeroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_app'

    def ready(self):
        from .signals import create_profile, save_profile
