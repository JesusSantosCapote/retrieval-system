import logging
from django.core.management import BaseCommand
from retrieval_system.core.models import Corpus
from retrieval_system.core.services import process_corpus

log = logging.getLogger()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("corpus", nargs="+", type=str)

    def handle(self, *args, **options):
        corpus_name = options["corpus"][0]
        try:
            corpus = Corpus.objects.get(name=corpus_name)
        except Corpus.DoesNotExist:
            log.error(f"Corpus {corpus_name} does not exist")
            return

        log.info(f"Running process corpus on {corpus_name}")

        process_corpus(corpus)

        log.info("Finished process corpus")
