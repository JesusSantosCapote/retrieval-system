import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import glob
import re
import os
import numpy as np
import sys
Stopwords = set(stopwords.words('english'))
nltk.download('punkt')

def remove_special_characters(text):
    regex = re.compile('[^a-zA-Z0-9\s]')
    text_returned = re.sub(regex,'',text)
    return text_returned

def files_indexer(file_folder):
    indexed_documents = {}
    doc_idx = 1

    for file in glob.glob(file_folder):
        fname = file
        file = open(file , "r")
        text = file.read()
        text = remove_special_characters(text)
        text = re.sub(re.compile('\d'),'',text)
        words = word_tokenize(text)
        words = [word for word in words if len(words)>1]
        words = [word.lower() for word in words]
        words = [word for word in words if word not in Stopwords]
        indexed_documents[doc_idx] = words
        doc_idx += 1

    return indexed_documents

def query_tokenizer(query):
    """
    Returns the set of tokens. Tokens can be separated by any number of blanks
    """
    query = re.split(r'\s+', query)
    tokens = [token.lower() for token in query]
    return tokens




#file_folder = "my_corpus/docs/*"

#print(files_indexer(file_folder))