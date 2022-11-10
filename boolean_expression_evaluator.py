import re

def query_tokenizer(query):
    query = re.split(r'\s+', query)
    print(query)

