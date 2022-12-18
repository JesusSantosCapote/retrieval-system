from retrieval_system.core.models import Document
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


def search(query: str, search_type: str):

    if search_type == "boolean":
        return __boolean_search(query)

    elif search_type == "vectorial":
        return __vectorial_search(query)

    elif search_type == "lsi":
        return __lsi_search(query)

    return []


def __boolean_search(query: str):

    query = query_tokenizer(query)

    documents = Document.objects.all()
    return evaluate(query, documents)


def __vectorial_search(query: str):

    query = query_tokenizer(query)
    query = get_query_tf(query)

    query_vector = get_query_vector(query)

    documents = Document.objects.all()
    documents_ranking = []

    for document in documents:
        doc_vector = get_doc_tf_idf_vector(document)
        cos = doc_query_cos(doc_vector, query_vector)
        documents_ranking.append((document, cos))

    documents_ranking.sort(key=lambda x: x[1], reverse=True)

    documents = [x[0] for x in documents_ranking]

    return documents


def __lsi_search(query: str):

    query = query_tokenizer(query)
    query = get_query_tf(query)

    docments_ranking = lsi_evaluate(query)

    return [document[0] for document in docments_ranking]
