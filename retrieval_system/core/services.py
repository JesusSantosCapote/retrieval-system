from .models import Document, Term, TermDocument

from retrieval_system.utils.document_indexer import tokenize_document
from retrieval_system.utils.vectorial_evaluator import calculate_tf_idf_matrix


def process_document(document: Document):

    document_tokens = tokenize_document(document.content)

    for token in document_tokens:

        term, _unused = Term.objects.get_or_create(key=token)

        term_document, created = TermDocument.objects.get_or_create(
            document=document, term=term
        )

        if created:
            term_document.count = 1
        else:
            term_document.count += 1
        term_document.tf = term_document.count / len(document_tokens)
        term_document.save()

    document.processed = True
    document.save()


def calculate_tf_idf():
    term_documents = TermDocument.objects.all()

    for term_document in term_documents:
        term_document.tf_idf = term_document.tf * term_document.term.idf
        term_document.save()

    calculate_tf_idf_matrix()
