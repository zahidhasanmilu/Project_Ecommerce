from django.db import models
import uuid
from django.utils.text import slugify

from django.urls import reverse
from django.conf import settings

##
from App_account.models import User
from App_shop.models import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='user_cart', on_delete=models.CASCADE)
    item = models.ForeignKey(
        Product, related_name='product_cart', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity}  X  {self.item}'

    def get_total(self):
        total = self.item.price * self.quantity
        float_total = format(total, '0.2f')
        return float_total

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


# Order Model
class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='user_orders', on_delete=models.CASCADE)
    orderitems = models.ManyToManyField(Cart)
    ordered = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    order_id = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order #{self.id} - {self.user}'

    def order_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += float(order_item.get_total())
        return total

    class Meta:
        db_table = 'order'
        managed = True
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
