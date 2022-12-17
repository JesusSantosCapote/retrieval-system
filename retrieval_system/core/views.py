from django.db.models import QuerySet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .selectors import search


from .serializers import DocumentSerializer
from .models import Document


class SearchDocumentsAPIView(ListAPIView):

    serializer_class = DocumentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self) -> QuerySet[Document]:
        query = self.request.query_params.get("query", None)
        if query:
            results = search(query, "boolean")
            return results
        return Document.objects.none()
