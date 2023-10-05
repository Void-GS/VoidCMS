from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    id = models.AutoField(primary_key=True)
    image = models.ForeignKey('Image', on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    #  Positioning
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children')
    # Meta
    meta_url = models.CharField(max_length=100, blank=True, unique=True)
    meta_title = models.CharField(max_length=100, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    class MPTTMeta:
        order_insertion_by = ['id']


    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.title
