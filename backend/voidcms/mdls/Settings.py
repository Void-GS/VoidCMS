from django.db import models
from django.core.validators import FileExtensionValidator

class Settings(models.Model):
    id = models.AutoField(primary_key=True)
    app_name = models.CharField(max_length=250, blank=False)
    app_url = models.CharField(max_length=250, blank=False)
    app_description = models.TextField(blank=True)
    app_background = models.ForeignKey('Image', on_delete=models.SET_NULL, blank=True, null=True, related_name='app_background')
    app_logo = models.ForeignKey('Image', on_delete=models.SET_NULL, blank=True, null=True, related_name='app_logo')
    app_favicon = models.ForeignKey('Image', on_delete=models.SET_NULL, blank=True, null=True, related_name='app_favicon')
    maintenance = models.BooleanField(default=False, blank=True)
