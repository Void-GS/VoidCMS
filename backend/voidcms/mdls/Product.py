from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Complectation(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100, blank=False)
    value = models.CharField(max_length=200, blank=False)
    price_change = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.type} - {self.value}"

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, blank=True, null=True,)
    images = models.ManyToManyField('Image', blank=True)
    visible = models.BooleanField(default=True, blank=True)
    is_promotioned = models.BooleanField(default=False, blank=True)

    complectations = models.ManyToManyField('Complectation', blank=True)

    # Meta
    meta_url = models.CharField(max_length=100, blank=True, unique=True)
    meta_title = models.CharField(max_length=100, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    def delete(self, *args, **kwargs):
        for complect in self.complectations.all():
            complect.delete()
        for image in self.images.all():
            image.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title


# @receiver(pre_delete, sender=Product.complectations.through)
# def remove_complectation_from_product(sender, instance, **kwargs):
#     instance.delete()
