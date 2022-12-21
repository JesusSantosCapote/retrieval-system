from django.contrib import admin
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter,
    RelatedDropdownFilter,
    ChoiceDropdownFilter,
)

from .models import Document, Term, TermDocument, Corpus

admin.site.site_title = "Retrieval System"
admin.site.site_header = "Retrieval System"


@admin.register(Corpus)
class CorpusAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "corpus"]
    search_fields = ["title", "author"]
    list_filter = [("corpus", RelatedDropdownFilter)]


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = [
        "key",
        "documents_count",
        "idf",
    ]
    search_fields = ["key"]


@admin.register(TermDocument)
class TermDocumentAdmin(admin.ModelAdmin):
    list_display = ["term", "document", "count", "tf", "tf_idf"]
    search_fields = ["term__key", "document__title"]
    autocomplete_fields = ["term", "document"]
    list_filter = [
        ("term", RelatedDropdownFilter),
        ("document", RelatedDropdownFilter),
    ]
