from django.shortcuts import render
from django.conf import settings
from elasticsearch import Elasticsearch
from django.http import JsonResponse
from django.views.decorators.http import require_GET


es = Elasticsearch(settings.ELASTICSEARCH_HOST)
INDEX_NAME = "books"

def index(request):
    return render(request, "books/index.html")

def search(request):
    q = request.GET.get("q", "").strip()
    results = []
    if q:
        body = {
            "query": {
                "multi_match": {
                    "query": q,
                    "fields": ["title^3"]
                }
            },
            "size": 20
        }
        try:
            res = es.search(index=INDEX_NAME, body=body)
            hits = res.get("hits", {}).get("hits", [])
            for h in hits:
                src = h["_source"]
                src["score"] = h.get("_score")
                results.append(src)
        except Exception as e:
            print("ES search error:", e)
    return render(request, "books/results.html", {"query": q, "results": results})

@require_GET
def suggest(request):
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse({"suggestions": []})

    body = {
        "size": 10,
        "query": {
            "multi_match": {
                "query": q,
                "fields": [
                    "title.autocomplete^3",
                    "author.autocomplete^2"
                ]
            }
        },
        "_source": ["title", "author"]
    }

    try:
        res = es.search(index=INDEX_NAME, body=body)
    except Exception as e:
        print("ES suggest error:", e)
        return JsonResponse({"suggestions": []})

    suggestions = []
    seen = set()

    for hit in res.get("hits", {}).get("hits", []):
        title = hit["_source"].get("title")
        author = hit["_source"].get("author")
        label = f"{title} — {author}" if author else title

        if title and title not in seen:
            suggestions.append({"title": title, "label": label})
            seen.add(title)

        if len(suggestions) >= 10:
            break

    return JsonResponse({"suggestions": suggestions})
