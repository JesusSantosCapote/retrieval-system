import numpy as np
import logging
from numpy.linalg import norm
from retrieval_system.core.models import Term, Document, TermDocument
from nltk.corpus import stopwords
from collections import Counter

Stopwords = set(stopwords.words("english"))

log = logging.getLogger()


def get_query_tf(tokenized_query):
    count = 0
    tokenized_query = [token for token in tokenized_query if token not in Stopwords]

    query_with_tf = Counter(tokenized_query)
    max_tf = 0
    for key in query_with_tf:
        tf = query_with_tf[key] / len(tokenized_query)
        query_with_tf[key] = tf
        max_tf = max(max_tf, tf)

    # Normalize tf
    for key in query_with_tf:
        query_with_tf[key] = query_with_tf[key] / max_tf

    terms = Term.objects.filter(key__in=query_with_tf.keys())

    query_with_tf = {
        terms.get(key=term): tf
        for term, tf in query_with_tf.items()
        if terms.filter(key=term).exists()
    }

    return query_with_tf


def get_query_vector(query, corpus):

    all_terms = enumerate(
        Term.objects.filter(term_documents__document__corpus=corpus).distinct()
    )
    all_terms_dict = {term: index for index, term in all_terms}

    query_vector = np.zeros(len(all_terms_dict))
    for term in query:
        if term in all_terms_dict.keys():
            query_vector[all_terms_dict[term]] = query[term] * term.idf

    return query_vector


def get_doc_tf_idf_vector(document: Document):

    return document.doc_vector


def doc_query_cos(doc, query):

    return np.dot(query, doc) / (norm(query) * norm(doc))


def calculate_tf_idf_matrix(corpus):

    all_terms = enumerate(
        Term.objects.filter(term_documents__document__corpus=corpus).distinct()
    )
    all_terms_dict = {term: index for index, term in all_terms}

    documents = corpus.documents.all()
    all_documents = enumerate(documents)
    all_documents_dict = {document: index for index, document in all_documents}

    tf_idf_matrix = {}

    for document in all_documents_dict.keys():
        tf_idf_matrix[document] = np.zeros(len(all_terms_dict))
        for term_document in document.term_documents.prefetch_related("term"):
            tf_idf_matrix[document][
                all_terms_dict[term_document.term]
            ] = term_document.tf_idf
        document.doc_vector = tf_idf_matrix[document]
        document.save()
        log.info(
            f"CALCULATED TF-IDF VECTOR FOR DOCUMENT {document.id} in corpus {corpus.name}"
        )

    return np.stack([document.doc_vector for document in documents])
