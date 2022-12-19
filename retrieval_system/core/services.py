import logging
from .models import Document, Term, TermDocument, Corpus

from retrieval_system.utils.document_indexer import tokenize_document
from retrieval_system.utils.vectorial_evaluator import calculate_tf_idf_matrix
from retrieval_system.utils.lsi import calculate_lsi

log = logging.getLogger()


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


def calculate_tf_idf(corpus):
    term_documents = TermDocument.objects.filter(
        document__corpus=corpus
    ).prefetch_related("term")

    for term_document in term_documents:
        term_document.tf_idf = term_document.tf * term_document.term.idf
        term_document.save()

    return calculate_tf_idf_matrix(corpus)


def process_corpus(corpus: Corpus):
    documents = corpus.documents.all()

    for document in documents:
        if not document.processed:
            process_document(document)

        log.info(f"Processed document {document.title}")

    log.info("Calculating tf-idf")
    corpus.tf_idf_matrix = calculate_tf_idf(corpus)

    corpus.save()

    log.info("Calculating LSI")
    T, S, dt_lsi_matrix, documents = calculate_lsi(corpus)
    corpus.t_lsi_matrix = T
    corpus.s_lsi_matrix = S
    corpus.dt_lsi_matrix = dt_lsi_matrix
    corpus.save()
