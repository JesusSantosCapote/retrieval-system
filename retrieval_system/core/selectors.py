from retrieval_system.core.models import Document
from retrieval_system.utils.document_indexer import query_tokenizer
from retrieval_system.utils.boolean_expression_evaluator import evaluate


def search(query: str, search_type: str):

    if search_type == "boolean":
        return __boolean_search(query)

    return []


def __boolean_search(query: str):

    query = query_tokenizer(query)

    documents = Document.objects.all()
    return evaluate(query, documents)