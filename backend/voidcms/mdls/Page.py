from django.db import models
from django.core.files.storage import default_storage

class Page(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False)
    content = models.TextField(blank=True)
    visible = models.BooleanField(default=True, blank=True)
    # Meta
    meta_url = models.CharField(max_length=100, blank=True, unique=True)
    meta_title = models.CharField(max_length=100, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)