import numpy as np
from numpy.linalg import norm
from retrieval_system.core.models import Document


def get_tf_idf_matrix():

    documents = Document.objects.all()

    tfidf_matrix = np.stack([document.doc_vector for document in documents])

    return tfidf_matrix, documents


def calculate_lsi():

    tfidf_matrix, documents = get_tf_idf_matrix()

    A = np.transpose(tfidf_matrix)

    T, S, DT = np.linalg.svd(A, full_matrices=False)
    print("SVD done")
    print("T shape: ", np.shape(T))
    print("S shape: ", np.shape(S))
    print("DT shape: ", np.shape(DT))
    minimum = min(np.shape(A))
    k = int(minimum * 60 / 100)

    DT = DT[: -(len(DT) - k)]

    for i in range(k, len(T[0])):
        T = np.delete(T, len(T[0]) - 1, axis=1)

    T = np.transpose(T)
    S = np.linalg.inv(S)
    DT = np.transpose(DT)

    return T, S, DT, documents


def evaluate(query):

    T, S, DT, documents = calculate_lsi()

    query_vec = np.transpose(np.dot(np.dot(T, S), np.transpose(query)))

    document_ranking = []

    for doc in range(np.shape(DT)[0]):
        doc_vector = DT[doc]
        doc_query_cos = np.dot(query_vec, doc_vector) / (
            norm(query_vec) * norm(doc_vector)
        )
        document_ranking.append((documents[doc], doc_query_cos))

    document_ranking.sort(key=lambda x: x[1], reverse=True)
    return document_ranking
