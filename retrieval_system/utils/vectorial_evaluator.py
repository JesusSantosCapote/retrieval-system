import numpy as np
from numpy.linalg import norm
from retrieval_system.core.models import Term, Document, TermDocument
from nltk.corpus import stopwords

Stopwords = set(stopwords.words("english"))


def get_query_tf(tokenized_query):
    count = 0
    tokenized_query = [token for token in tokenized_query if token not in Stopwords]
    query_with_tf = {}

    for word in tokenized_query:
        for i in range(len(tokenized_query)):
            if word == tokenized_query[i]:
                count += 1
        query_with_tf[word] = count / len(tokenized_query)
        count = 0

    terms = Term.objects.filter(key__in=query_with_tf.keys())

    query_with_tf = {
        terms.get(key=term): index
        for term, index in query_with_tf.items()
        if terms.filter(key=term).exists()
    }

    return query_with_tf


def get_query_vector(query):

    all_terms = enumerate(Term.objects.all())
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


def calculate_tf_idf_matrix():

    all_terms = enumerate(Term.objects.all())
    all_terms_dict = {term: index for index, term in all_terms}

    all_documents = enumerate(Document.objects.all())
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
        print(f"CALCULATED TF-IDF VECTOR FOR DOCUMENT {document.id}...")

    return tf_idf_matrix
