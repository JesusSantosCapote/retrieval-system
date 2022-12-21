from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from retrieval_system.users.api.views import UserViewSet
from retrieval_system.core.views import SearchDocumentsAPIView, CorpusListView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path("search/", SearchDocumentsAPIView.as_view(), name="search"),
    path("corpus/", CorpusListView.as_view(), name="corpus-list"),
]
