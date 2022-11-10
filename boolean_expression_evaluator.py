import re

def query_tokenizer(query):
    """
    Returns the set of tokens. Tokens can be separated by any number of blanks
    """
    query = re.split(r'\s+', query)
    tokens = [token.lower() for token in query]
    return tokens


# These lambda expressions map from operators to actual executable code
operations = {
    'and': lambda x,y: x and y,
    'or': lambda x,y: x or y,
    'not': lambda x: not x,
}

