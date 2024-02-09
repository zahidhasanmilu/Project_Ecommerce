from django.db import models
import uuid
from django.utils.text import slugify

from django.urls import reverse

# Create your models here.


class Category(models.Model):
    name = models.CharField(unique=True, max_length=100,
                            blank=False, null=False)
    slug = models.SlugField(unique=True, blank=True, max_length=300)
    image = models.ImageField(
        upload_to='Category_Images/', blank=True, null=True)
    parent = models.ForeignKey(
        'self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        ordering = ['-created',]
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    def save(self, *args, **kwargs):
        # Generate slug using the product name
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(unique=True, blank=True, max_length=300)
    category = models.ForeignKey(
        'Category', related_name='category_product', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='Product_Images/', blank=False, null=False)
    preview_description = models.TextField(blank=True, null=True)
    full_description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0.00)
    old_price = models.FloatField(default=0.00, blank=True, null=True)
    is_stock = models.BooleanField(default=True,)
    created = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Generate slug using the product name
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        
    def get_product_url(self):
        
        return reverse('product_details', kwargs={'slug': self.slug})
    
    
class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Product_gellary")
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return str(self.product.name)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'ProductImage'
        verbose_name_plural = 'ProductImages'
