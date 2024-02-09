from django.contrib import admin
from App_shop.models import Category, Product,ProductImage

# Register your models here.
class ProductImageAdmin(admin.TabularInline):  # or use admin.StackedInline for a stacked layout
    model = ProductImage
    # extra = 1  # Number of empty forms to display

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
    prepopulated_fields = {'slug':('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_stock', 'created')
    prepopulated_fields = {'slug':('name',)}
    inlines = [ProductImageAdmin]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
