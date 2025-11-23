# web/books/management/commands/reindex_books.py
from django.core.management.base import BaseCommand
from django.conf import settings
from elasticsearch import Elasticsearch
from books.models import Book

INDEX_NAME = "books"

def book_to_doc(book: Book):
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "summary": book.summary,
        "tags": [t.strip() for t in (book.tags or "").split(",") if t.strip()],
        "published_date": book.published_date.isoformat() if book.published_date else None,
    }

class Command(BaseCommand):
    help = "Reindex all Book objects into Elasticsearch"

    def handle(self, *args, **options):
        es = Elasticsearch(settings.ELASTICSEARCH_HOST)
        qs = Book.objects.all()
        count = qs.count()
        self.stdout.write(f"Reindexing {count} books...")
        for book in qs:
            es.index(index=INDEX_NAME, id=book.id, body=book_to_doc(book))
        es.indices.refresh(index=INDEX_NAME)
        self.stdout.write(self.style.SUCCESS("Reindex complete"))
