import logging

from django.core.management import BaseCommand
from retrieval_system.core.models import Document
from retrieval_system.core.services import process_document, calculate_tf_idf

log = logging.getLogger()


class Command(BaseCommand):
    def handle(self, *args, **options):
        log.info("Running process documents command")

        documents = Document.objects.filter(processed=False)

        for document in documents:
            process_document(document)
            log.info(f"Processed document {document.title}")

        log.info("Finished processing documents")

        log.info("Calculating TF-IDF")
        calculate_tf_idf()
        log.info("Finished calculating TF-IDF")
