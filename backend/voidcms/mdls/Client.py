from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from voidcms.mdls.Cart import Cart

class Client(AbstractUser):
    ADMIN = 'admin'
    USER = 'user'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (USER, 'User'),
    ]
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER)
    name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, unique=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.id: 
            super().save(*args, **kwargs)
            Cart.objects.create(client=self)
        else:
            super().save(*args, **kwargs)

