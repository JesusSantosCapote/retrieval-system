from retrieval_system.core.models import Document, Corpus
from retrieval_system.utils.document_indexer import (
    query_tokenizer,
)
from retrieval_system.utils.boolean_expression_evaluator import evaluate
from retrieval_system.utils.vectorial_evaluator import (
    get_query_tf,
    get_query_vector,
    get_doc_tf_idf_vector,
    doc_query_cos,
)
from retrieval_system.utils.lsi import evaluate as lsi_evaluate


def search(query: str, search_type: str, corpus: Corpus):

    if search_type == "boolean":
        return __boolean_search(query, corpus)

    elif search_type == "vectorial":
        return __vectorial_search(query, corpus)

    elif search_type == "lsi":
        return __lsi_search(query, corpus)

    return []


def __boolean_search(query: str, corpus: Corpus):

    query = query_tokenizer(query)

    documents = corpus.documents.all()
    return evaluate(query, documents)


def __vectorial_search(query: str, corpus: Corpus):

    query = query_tokenizer(query)
    query = get_query_tf(query)

    query_vector = get_query_vector(query, corpus)

    documents = {
        index: document for index, document in enumerate(corpus.documents.all())
    }
    documents_ranking = []

    for index, document in documents.items():
        doc_vector = corpus.tf_idf_matrix[index]
        cos = doc_query_cos(doc_vector, query_vector)
        documents_ranking.append((document, cos))

    documents_ranking.sort(key=lambda x: x[1], reverse=True)

    documents = [document for document, rank in documents_ranking if rank >= 0.5]

    return documents


def __lsi_search(query: str, corpus: Corpus):

    query = query_tokenizer(query)
    query = get_query_tf(query)

    query_vector = get_query_vector(query, corpus)
    documents_ranking = lsi_evaluate(query_vector, corpus)

    return [document for document, rank in documents_ranking if rank >= 0.5]
