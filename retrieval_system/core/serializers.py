from rest_framework import serializers

from .models import Document, Corpus


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "title", "file", "author", "corpus_index", "content"]


class CorpusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corpus
        fields = ["id", "name"]
