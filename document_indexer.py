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
nltk.download('punkt')

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
    term_index = tfidf.vocabulary_

    return term_index, result


def query_tokenizer(query):
    """
    Returns the set of tokens. Tokens can be separated by any number of blanks
    """
    query = re.split(r'\s+', query)
    tokens = [token.lower() for token in query]
    return tokens