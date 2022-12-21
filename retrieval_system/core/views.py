from django.db.models import QuerySet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .selectors import search


from .serializers import DocumentSerializer, CorpusSerializer
from .models import Document, Corpus


class SearchDocumentsAPIView(ListAPIView):

    serializer_class = DocumentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self) -> QuerySet[Document]:
        query = self.request.query_params.get("query", None)
        type = self.request.query_params.get("type", "vectorial")
        corpus = self.request.query_params.get("corpus", "all")

        corpus = Corpus.objects.get(name=corpus)

        if query:
            results = search(query, type, corpus)
            return results
        return Document.objects.none()


class CorpusListView(ListAPIView):
    serializer_class = CorpusSerializer
    permission_classes = [AllowAny]
    queryset = Corpus.objects.all()
