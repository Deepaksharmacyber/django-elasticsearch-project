from django.conf import settings
from django.db.backends.dummy.base import ignore
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from elasticsearch import Elasticsearch
from .models import Book
import json

es = Elasticsearch(settings.ELASTICSEARCH_HOST)

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

@receiver(post_save, sender=Book)
def index_book(sender, instance, **kwargs):
    try:
        es.index(index=INDEX_NAME, id=instance.id, body=book_to_doc(instance))
    except Exception as e:
        # in dev, you may log this; do not crash the request
        print("ES index error:", e)


@receiver(post_delete, sender=Book)
def delete_book(sender, instance, **kwargs):
    try:
        es.delete(index=INDEX_NAME, id=instance.id, ignore=[404])
    except Exception as e:
        print("ES delete error:", e)


