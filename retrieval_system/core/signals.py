from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Document
from .services import process_document, calculate_tf_idf


@receiver(post_save, sender=Document)
def document_post_save(sender, instance, created, **kwargs):
    if created:
        process_document(instance)
        calculate_tf_idf()


@receiver(post_delete, sender=Document)
def document_post_delete(sender, instance, **kwargs):
    calculate_tf_idf()
