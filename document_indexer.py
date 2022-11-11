import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import sent_tokenize , word_tokenize
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

    for file in glob.glob(file_folder):
        print(file)
        fname = file
        file = open(file , "r")
        text = file.read()
        text = remove_special_characters(text)
        text = re.sub(re.compile('\d'),'',text)
        words = word_tokenize(text)
        words = [word for word in words if len(words)>1]
        words = [word.lower() for word in words]
        words = [word for word in words if word not in Stopwords]
        indexed_documents[fname] = words

    return indexed_documents


file_folder = "my_corpus/docs/*"

print(files_indexer(file_folder))