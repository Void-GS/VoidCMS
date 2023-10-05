from django.db import models

class Social(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=250, blank=False)
    url = models.CharField(max_length=250, blank=False)