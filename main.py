from document_indexer import query_tokenizer, extract_text_from_files, tokenize_documents, get_tfidf_matrix, get_query_tf
from boolean_expression_evaluator import evaluate
import numpy
from numpy.linalg import norm
import scipy


def run_boolean_model(documents):
    print('Type a query in boolean expresion form')
    query = input()
    query = query_tokenizer(query)
    output = []

    for file in documents.keys():
        if evaluate(query, documents[file]):
            output.append(file)

    return output


def run_vectorial_model(file_folder, query):
    docs = extract_text_from_files(file_folder)
    term_indexes, terms_idf, tfidf_matrix = get_tfidf_matrix(docs)
    query = query_tokenizer(query)
    query_with_tf = get_query_tf(query)

    for query_term in query_with_tf.keys():
        if query_term not in term_indexes.keys():
            query_with_tf.pop(query_term)

    query_vector = numpy.zeros(len(term_indexes))

    for term in query_with_tf.keys():
        query_vector[term_indexes[term]] = query_with_tf[term] * terms_idf[term]

    ranking = []

    doc_count =  numpy.shape(tfidf_matrix)[0]
    tfidf_matrix = scipy.sparse.csr_matrix.toarray(order=None, out=None)[tfidf_matrix]
    print(tfidf_matrix)

    for doc in range(doc_count):
        doc_vector = tfidf_matrix[doc]
        doc_query_cos = numpy.dot(query_vector, doc_vector) / (norm(query_vector) * norm(doc_vector))
        ranking.append((doc+1, doc_query_cos))

    ranking.sort(key=lambda x: x[1])

    return ranking



query = "experimental study of a wing"


files_folders = ['splitted_cranfieldDocs/*']

print(run_vectorial_model(files_folders[0], query))

# documents = extract_text_from_files(files_folders[0])

# tokenized_documents = tokenize_documents(documents)

# print(run_boolean_model(tokenized_documents))


