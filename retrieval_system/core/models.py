from django.db import models
from math import log

from picklefield.fields import PickledObjectField


class Document(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(default="", blank=True)
    file = models.FileField(upload_to="documents/")
    author = models.CharField(max_length=200)
    processed = models.BooleanField(default=False)

    doc_vector = PickledObjectField(default=list, editable=False, blank=True)

    def __str__(self) -> str:
        return self.title


class Term(models.Model):
    key = models.CharField(max_length=200, unique=True)

    @property
    def documents_count(self):
        """Number of documents that contains this term"""
        return self.term_documents.count()

    @property
    def idf(self):
        """Inverse document frequency"""
        total_documents = Document.objects.all().count()
        return log(total_documents / (self.documents_count + 1))

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
