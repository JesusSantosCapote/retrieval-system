import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import glob
import re
import os
import numpy as np
import sys
from sklearn.feature_extraction.text import TfidfVectorizer

Stopwords = set(stopwords.words('english'))
#nltk.download('punkt')

def remove_special_characters(text):
    regex = re.compile('[^a-zA-Z0-9\s]')
    text_returned = re.sub(regex,'',text)
    return text_returned
    

def extract_text_from_files(file_folder):
    docs = []
    for file in glob.glob(file_folder):
        file = open(file , "r")
        text = file.read()
        text = remove_special_characters(text)
        text = re.sub(re.compile('\d'),'',text)
        docs.append(text)

    return docs


def tokenize_documents(document_list):
    tokenized_documents = {}
    doc_idx = 1

    for doc in document_list:
        words = word_tokenize(doc)
        words = [word for word in words if len(words)>1]
        words = [word.lower() for word in words]
        words = [word for word in words if word not in Stopwords]
        tokenized_documents[doc_idx] = words
        doc_idx += 1

    return tokenized_documents


def get_tfidf_matrix(docs):
    """
    Returns a matrix where the position i,j store the value tf*idf of the term j in the document i and
    a 'term_index' which is a dictionary where keys are the terms and values are the column of the term in the matrix.
    """
    tfidf = TfidfVectorizer()
    result = tfidf.fit_transform(docs)
    term_indexes = tfidf.vocabulary_
    terms_idf = {}

    for ele1, ele2 in zip(tfidf.get_feature_names(), tfidf.idf_):
        terms_idf[ele1] = ele2

    return term_indexes, terms_idf, result


def query_tokenizer(query):
    """
    Returns the set of tokens. Tokens can be separated by any number of blanks
    """
    query = re.split(r'\s+', query)
    tokens = [token.lower() for token in query]
    return tokens


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

    return query_with_tf
