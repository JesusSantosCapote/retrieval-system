import logging
import json
from django.core.management import BaseCommand
from django.core.files.base import ContentFile
from retrieval_system.core.models import Document, Corpus

log = logging.getLogger()


class Command(BaseCommand):
    def handle(self, *args, **options):
        log.info("Running insert cranfield files command")

        insert_cranfield_files()

        log.info("Finished insert cranfield files")


def insert_cranfield_files():

    path = "./datasets/cranfield/CRAN.ALL.json"

    with open(path) as f:
        data = json.load(f)

    corpus, created = Corpus.objects.get_or_create(name="cranfield")
    for i in range(len(data)):

        corpus_index = i + 1
        index = str(corpus_index)

        title = data[index]["title"]
        text = data[index]["abstract"]

        try:
            author = data[index]["author"]
        except KeyError:
            author = "Unknown"

        file = ContentFile(text.encode("utf-8"), name="cranfield" + index + ".txt")

        # create a document object
        Document.objects.create(
            title=title,
            content=text,
            author=author,
            file=file,
            corpus=corpus,
            corpus_index=corpus_index,
        )

        log.info(f"Saved document: {title:30} on corpus: {corpus.name}")

    corpus.save()
