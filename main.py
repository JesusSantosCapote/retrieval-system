from document_indexer import query_tokenizer, extract_text_from_files, tokenize_documents
from boolean_expression_evaluator import evaluate

def run_boolean_model(documents):
    print('Type a query in boolean expresion form')
    query = input()
    query = query_tokenizer(query)
    output = []

    for file in documents.keys():
        if evaluate(query, documents[file]):
            output.append(file)

    return output


files_folders = ['splitted_cranfieldDocs/*']

documents = extract_text_from_files(files_folders[0])

tokenized_documents = tokenize_documents(documents)

print(run_boolean_model(tokenized_documents))


