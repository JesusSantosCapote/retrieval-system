from retrieval_system.utils.document_indexer import query_tokenizer


def search(query: str, search_type: str):

    if search_type == "boolean":
        return __boolean_search(query)

    return []


def __boolean_search(query: str):

    query = query_tokenizer(query)

    return []
