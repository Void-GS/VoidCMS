from django.db import models
from django.db.models.signals import m2m_changed, pre_delete
from django.dispatch import receiver
from decimal import Decimal
import json


from django.core.validators import MinValueValidator, MaxValueValidator

STATUS_CHOICES = [
    ('paperwork', 'Paperwork'),
    ('payment', 'Payment'),
    ('processing', 'Processing'),
    ('shipping', 'Shipping'),
    ('done', 'Done'),
    ('canceled', 'Canceled'),
]


class OrderProduct(models.Model):
    title = models.CharField(max_length=100, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    meta_url = models.CharField(max_length=100, blank=True)


class OrderItem(models.Model):
    product = models.ForeignKey(
        'OrderProduct', on_delete=models.CASCADE)

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


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default='payment')
    order_name = models.CharField(max_length=256)
    order_phone = models.CharField(max_length=20)
    order_address = models.CharField(max_length=512)
    order_comment = models.TextField(blank=True)
    track_info = models.TextField(blank=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    was_viewed = models.BooleanField(default=False, blank=True)

    items = models.ManyToManyField(OrderItem)

    def save(self, *args, **kwargs):
        self.viewed = False
        super(Order, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.items.all().delete()
        super().delete(*args, **kwargs)


@receiver(m2m_changed, sender=Order.items.through)
def calculate_total_price(sender, instance, action, pk_set, **kwargs):
    for item in instance.items.all():
        product_price = item.product.price
        for complectation in item.complectations:
            product_price += Decimal(complectation['price_change'])
        instance.total_price += product_price * item.count
    instance.save()
