from django.db.models import QuerySet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from .selectors import search


from .serializers import DocumentSerializer
from .models import Document


class SearchDocumentsAPIView(ListAPIView):

    serializer_class = DocumentSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def get_queryset(self) -> QuerySet[Document]:
        query = self.request.query_params.get("query", None)
        type = self.request.query_params.get("type", "vectorial")
        if query:
            results = search(query, type)
            return results
        return Document.objects.none()
