from django.contrib import admin
from App_payment.models import Checkout

# Register your models here.


class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address', 'order_note',)


admin.site.register(Checkout,CheckoutAdmin)
