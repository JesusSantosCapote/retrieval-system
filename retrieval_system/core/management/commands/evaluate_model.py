import logging
from django.core.management import BaseCommand
from retrieval_system.core.models import Corpus
from retrieval_system.core.selectors import search
from retrieval_system.core.utils import load_queries
from retrieval_system.utils.document_indexer import preprocess_boolean_query

log = logging.getLogger()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("corpus", type=str)
        parser.add_argument("model", type=str)
        parser.add_argument("query", type=str)
        parser.add_argument("rel", type=str)
        parser.add_argument("measure", type=str)

    def handle(self, *args, **options):
        corpus_name = options["corpus"]
        model_name = options["model"]
        query_path = options["query"]
        rel_path = options["rel"]
        measure = options["measure"]
        try:
            corpus = Corpus.objects.get(name=corpus_name)
        except Corpus.DoesNotExist:
            log.error(f"Corpus {corpus_name} does not exist")
            return
        if model_name not in ("boolean", "vectorial", "lsi"):
            log.error(f"Model {model_name} does not exist")
            log.error("Available models: boolean, vectorial, lsi")
            return

        if measure not in ("precision", "recall", "f1"):
            log.error(f"Measure {measure} does not exist")
            log.error("Available measures: precision, recall, f1")
            return

        log.info(
            f"Running evaluation on Corpus {corpus_name} with model {model_name} using {measure} measure"
        )

        queries = load_queries(query_path, rel_path)

        measure_dict = {
            "precision": lambda x: x.evaluate_precision,
            "recall": lambda x: x.evaluate_recall,
            "f1": lambda x: x.evaluate_f1,
        }
        total_measure = 0
        for query in queries:

            if model_name == "boolean":
                query.query = preprocess_boolean_query(query.query)
            documents = search(query.query, model_name, corpus)
            score = measure_dict[measure](query)(documents)
            log.info(f"Query {query.id} {measure}: {score}")
            total_measure += score

        log.info(f"Average {measure}: {total_measure / len(queries)}")

        log.info("Finished process corpus")
