import re

def query_tokenizer(query):
    """
    Returns the set of tokens. Tokens can be separated by any number of blanks
    """

    query = re.split(r'\s+', query)
    tokens = [token.lower() for token in query]
    return tokens
