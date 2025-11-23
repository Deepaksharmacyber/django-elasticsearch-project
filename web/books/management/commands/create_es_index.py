# web/books/management/commands/create_es_index.py
from django.core.management.base import BaseCommand
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError

INDEX_NAME = "books"

MAPPING = {
    "settings": {
        "analysis": {
            "filter": {
                "autocomplete_filter": {
                    "type": "edge_ngram",
                    "min_gram": 1,
                    "max_gram": 20
                }
            },
            "analyzer": {
                "autocomplete": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "autocomplete_filter"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "title": {
                "type": "text",
                # normal full-text for regular search
                "analyzer": "standard",
                "fields": {
                    # autocomplete subfield
                    "autocomplete": {
                        "type": "text",
                        "analyzer": "autocomplete",
                        "search_analyzer": "standard"
                    },
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "author": {
                "type": "text",
                "fields": {
                    "autocomplete": {
                        "type": "text",
                        "analyzer": "autocomplete",
                        "search_analyzer": "standard"
                    },
                    "keyword": {"type": "keyword"}
                }
            },
            "summary": {"type": "text"},
            "tags": {"type": "keyword"},
            "published_date": {"type": "date"}
        }
    }
}

class Command(BaseCommand):
    help = "Create Elasticsearch index with mapping for books (with autocomplete)"

    def handle(self, *args, **options):
        es = Elasticsearch(settings.ELASTICSEARCH_HOST)
        # delete if exists (optional) and create new
        if es.indices.exists(index=INDEX_NAME):
            self.stdout.write(self.style.WARNING(f"Index '{INDEX_NAME}' exists — deleting it first"))
            es.indices.delete(index=INDEX_NAME, ignore=[400, 404])
        try:
            es.indices.create(index=INDEX_NAME, body=MAPPING)
            self.stdout.write(self.style.SUCCESS(f"Created index '{INDEX_NAME}' with autocomplete mapping"))
        except RequestError as e:
            self.stdout.write(self.style.ERROR(f"Error creating index: {e.info if hasattr(e,'info') else e}"))
