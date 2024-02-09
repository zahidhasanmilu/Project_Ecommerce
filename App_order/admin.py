from django.contrib import admin
from App_order.models import Cart, Order


# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('item','quantity','display_total','purchased','created')
    
    def display_total(self, obj):
        return obj.get_total()

    display_total.short_description = 'Total'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_summary','order_totals','ordered','payment_id','order_id','created')
    
    def order_summary(self, obj):
        return ", ".join([f"{item.quantity} X {item.item}" for item in obj.orderitems.all()])

    def order_totals(self, obj):
        return obj.order_totals()

    order_summary.short_description = 'Order Items'
    order_totals.short_description = 'Order Total'

admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
