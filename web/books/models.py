from django.db import models

# Create your models here.
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=400)
    author = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    tags = models.CharField(max_length=200, blank=True)  # comma-separated
    published_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} — {self.author}"
