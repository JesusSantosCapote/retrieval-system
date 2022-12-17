from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "retrieval_system.core"

    def ready(self):

        from .signals import document_post_save, document_post_delete
