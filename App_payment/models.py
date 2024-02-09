from django.db import models
import uuid
from django.utils.text import slugify

from django.urls import reverse
from django.conf import settings

##
from App_account.models import User
from App_shop.models import Product

# Create your models here.

class Checkout(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    address = models.TextField()
    order_note = models.TextField()
    
    
    def __str__(self):
        return self.name
    

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Checkout'
        verbose_name_plural = 'Checkouts'