from document_indexer import query_tokenizer, extract_text_from_files, tokenize_documents, get_tfidf_matrix, get_query_tf
from boolean_expression_evaluator import evaluate
import numpy
from numpy.linalg import norm
import scipy


def run_boolean_model(files_folder, query):
    documents = extract_text_from_files(files_folder)
    tokenized_documents = tokenize_documents(documents)
    query = query_tokenizer(query)
    output = []

    for file in tokenized_documents.keys():
        if evaluate(query, documents[file]):
            output.append(file)

    return output


def run_vectorial_model(files_folder, query):
    docs = extract_text_from_files(files_folder)
    term_indexes, terms_idf, tfidf_matrix = get_tfidf_matrix(docs)
    query = query_tokenizer(query)
    query_with_tf = get_query_tf(query)

    temp = {}
    for query_term in query_with_tf.keys():
        if query_term in term_indexes.keys():
            temp[query_term] = query_with_tf[query_term]

    query_with_tf = temp

    query_vector = numpy.zeros(len(term_indexes))

    for term in query_with_tf.keys():
        query_vector[term_indexes[term]] = query_with_tf[term] * terms_idf[term]

    ranking = []

    doc_count =  numpy.shape(tfidf_matrix)[0]
    tfidf_matrix = scipy.sparse.csr_matrix.toarray(tfidf_matrix ,order=None, out=None)

    for doc in range(doc_count):
        doc_vector = tfidf_matrix[doc]
        doc_query_cos = numpy.dot(query_vector, doc_vector) / (norm(query_vector) * norm(doc_vector))
        ranking.append((doc+1, doc_query_cos))

    ranking.sort(key=lambda x: x[1], reverse=True)

    return ranking

def run_LSI_model(files_folder, query):
    docs = extract_text_from_files(files_folder)
    term_indexes, terms_idf, tfidf_matrix = get_tfidf_matrix(docs)
    query = query_tokenizer(query)
    query_with_tf = get_query_tf(query)

    temp = {}
    for query_term in query_with_tf.keys():
        if query_term in term_indexes.keys():
            temp[query_term] = query_with_tf[query_term]

    query_with_tf = temp

    query_vector = numpy.zeros(len(term_indexes))

    for term in query_with_tf.keys():
        query_vector[term_indexes[term]] = query_with_tf[term] * terms_idf[term]

    A = numpy.transpose(tfidf_matrix)
    T, S , DT = numpy.linalg.svd(A, full_matrices= False)
    min = min(numpy.shape(A))
    k = int(min*60/100)
    DT = DT[:-(len(DT)-k)]
    for i in range(k,len(T[0])):
        T = numpy.delete(T,len(T[0])-1,axis=1)
    T = numpy.transpose(T)
    S = numpy.linalg.inv(S)
    query_vector_lsi = numpy.transpose( numpy.dot( numpy.dot(T,S), numpy.transpose(query_vector) ) )

    ranking = []




    



# query = "How can actually pertinent data, as opposed to references or entire articles themselves, be retrieved automatically in response to information requests?"


# files_folders = ['splitted_cisi/*']

# print(run_vectorial_model(files_folders[0], query))

# documents = extract_text_from_files(files_folders[0])

# tokenized_documents = tokenize_documents(documents)

# print(run_boolean_model(tokenized_documents))


