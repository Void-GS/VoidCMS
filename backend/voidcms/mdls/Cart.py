from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
import json


class CartItem(models.Model):
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, blank=True, null=True)

    complectations = models.JSONField(default=list, blank=True)

    count = models.IntegerField(
        validators=[
            MinValueValidator(1, message='Count must be at least 1.'),
            MaxValueValidator(99, message='Count cannot exceed 99.')
        ],
        default=1
    )

    def update_complectations(self):
        complectations_list = self.complectations_list()
        self.complectations = json.dumps(complectations_list)

    def complectations_list(self):
        return json.loads(self.complectations)


class Cart(models.Model):
    items = models.ManyToManyField('CartItem', blank=True)
    client = models.OneToOneField(
        'Client', on_delete=models.CASCADE, primary_key=True)


@receiver(m2m_changed, sender=Cart.items.through)
def remove_cartitem(sender, instance, action, pk_set, **kwargs):
    if action == "post_remove":
        CartItem.objects.filter(pk__in=pk_set).delete()
