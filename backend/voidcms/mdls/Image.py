from django.db import models
from django.core.files.storage import default_storage
from django.core.validators import FileExtensionValidator


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False)
    url = models.FileField(
        upload_to="images/",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['ico', 'jpg', 'jpeg', 'png', 'svg', 'mp4', 'gif', 'webm', 'webp'])]
    )

    def delete(self, *args, **kwargs):
        if self.url:
            default_storage.delete(self.url.name)
        
        super().delete(*args, **kwargs)