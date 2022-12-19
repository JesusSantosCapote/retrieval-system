import json
from typing import Iterable


class QueryRel:
    def __init__(self, id, query, rel) -> None:
        self.id = id
        self.query = query
        self.rel = rel

    def evaluate_precision(self, results):
        relevant = 0
        for result in results:
            if str(result.corpus_index) in self.rel:
                relevant += 1
        if len(results) == 0:
            return 0
        return relevant / len(results)

    def evaluate_recall(self, results):
        relevant = 0
        for result in results:
            if str(result.corpus_index) in self.rel:
                relevant += 1
        return relevant / len(self.rel)

    def evaluate_f1(self, results):
        precision = self.evaluate_precision(results)
        recall = self.evaluate_recall(results)
        return 2 * precision * recall / (precision + recall)


def load_queries(qpath, rpath) -> Iterable[QueryRel]:
    queries = []
    with open(qpath, "r") as f:
        data_query = json.load(f)
    with open(rpath, "r") as f:
        data_rel = json.load(f)

    for q in data_query:
        query = data_query[q]
        queries.append(QueryRel(query["id"], query["text"], data_rel[q]))

    return queries
