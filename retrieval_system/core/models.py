from django.db import models
from math import log

from picklefield.fields import PickledObjectField


class Corpus(models.Model):
    name = models.CharField(max_length=200)

    tf_idf_matrix = PickledObjectField(default=list, editable=False, blank=True)
    t_lsi_matrix = PickledObjectField(default=list, editable=False, blank=True)
    s_lsi_matrix = PickledObjectField(default=list, editable=False, blank=True)
    dt_lsi_matrix = PickledObjectField(default=list, editable=False, blank=True)

    def __str__(self) -> str:
        return self.name


class Document(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(default="", blank=True)
    file = models.FileField(upload_to="documents/")
    author = models.CharField(max_length=200)
    processed = models.BooleanField(default=False)
    corpus = models.ForeignKey(
        Corpus,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="documents",
    )

    corpus_index = models.IntegerField(default=0, editable=False)

    def __str__(self) -> str:
        return self.title


class Term(models.Model):
    key = models.CharField(max_length=200, unique=True)

    def documents_count(self, corpus):
        """Number of documents that contains this term"""
        return self.term_documents.filter(document__corpus=corpus).count()

    def idf(self, corpus):
        """Inverse document frequency"""
        total_documents = Document.objects.filter(corpus=corpus).count()
        return log(total_documents / (self.documents_count(corpus) + 1))

    def __str__(self) -> str:
        return self.key


class TermDocument(models.Model):
    term = models.ForeignKey(
        Term, on_delete=models.CASCADE, related_name="term_documents"
    )
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="term_documents"
    )
    count = models.IntegerField(default=0, editable=False)
    tf = models.FloatField(editable=False, default=0)

    tf_idf = models.FloatField(editable=False, default=0)

    def __str__(self) -> str:
        return f"{self.term} - {self.document}"
