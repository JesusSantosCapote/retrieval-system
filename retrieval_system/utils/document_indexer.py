from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

Stopwords = set(stopwords.words("english"))


def remove_special_characters(text):
    regex = re.compile("[^a-zA-Z0-9\s]")
    text_returned = re.sub(regex, "", text)
    return text_returned


def extract_text_from_file(file):
    file = open(file, "r")
    text = file.read()
    text = remove_special_characters(text)
    text = re.sub(re.compile("\d"), "", text)
    return text


def tokenize_document(doc):

    words = remove_special_characters(doc)
    words = re.sub(re.compile("\d"), "", words)
    words = word_tokenize(words)
    words = [word.strip() for word in words if len(words) > 1]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in Stopwords]
    return words


def query_tokenizer(query):
    """
    Returns the set of tokens. Tokens can be separated by any number of blanks
    """
    query = re.split(r"\s+", query)
    tokens = [token.lower() for token in query]
    return tokens


def preprocess_query(query):
    words = remove_special_characters(query)
    words = re.sub(re.compile("\d"), "", words)
    words = word_tokenize(words)
    words = [word.strip() for word in words if len(words) > 1]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in Stopwords]
    return " ".join(words)


def preprocess_boolean_query(query):

    words = remove_special_characters(query)
    words = re.sub(re.compile("\d"), "", words)
    words = word_tokenize(words)
    words = [word.strip() for word in words if len(words) > 1]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in Stopwords]

    return " and ".join(words)
