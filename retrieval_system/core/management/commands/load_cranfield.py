import logging
import os
from django.core.management import BaseCommand
from django.core.files.base import ContentFile
from retrieval_system.core.models import Document, Corpus
from retrieval_system.core.services import process_document, calculate_tf_idf
from retrieval_system.core.utils import parse_cranfield_file

log = logging.getLogger()


class Command(BaseCommand):
    def handle(self, *args, **options):
        log.info("Running insert cranfield files command")

        insert_cranfield_files()

        log.info("Finished insert cranfield files")


def insert_cranfield_files():

    folder_path = "cranfieldDocs"

    filenames = os.listdir(folder_path)
    corpus, created = Corpus.objects.get_or_create(name="cranfield")
    for fname in filenames:

        # generate filenames
        infilepath = folder_path + "/" + fname

        title, text, author = parse_cranfield_file(infilepath)

        content = f"{title}\n{author}\n{text}"

        file = ContentFile(content.encode("utf-8"), name=fname)

        # create a document object
        Document.objects.create(
            title=title, content=text, author=author, file=file, corpus=corpus
        )

        log.info(f"Saved document: {title:30} on corpus: {corpus.name}")

    corpus.save()
