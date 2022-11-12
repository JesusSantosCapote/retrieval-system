from document_indexer import query_tokenizer, files_indexer
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




def main():
    files_folders = ['cranfieldDocs/*']

    documents = files_indexer(files_folders[0])

    print(run_boolean_model(documents))

main()

