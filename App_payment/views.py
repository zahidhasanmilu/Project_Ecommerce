from django.conf import settings
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect, HttpResponse
from django.urls import reverse, reverse_lazy

# VIEW
from django.views.generic import CreateView, ListView, DetailView, UpdateView, View, TemplateView, DeleteView

# Authentication
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

# forms
from django.contrib.auth.forms import AuthenticationForm

# models
from App_account.models import User, Profile
from App_order.models import Order,Cart
from App_payment.models import Checkout

# forms
from App_account.forms import SignUpForm
from App_payment.forms import CheckoutForm,PaymentMethodForm

# message
from django.contrib import messages

import uuid
from django.db.models import Q

#for SSL COMMERZ
from decimal import Decimal
from sslcommerz_python.payment import SSLCSession


# Create your views here.

# class CheckoutView(View):
#     def get(self, request, *args, **kwargs):
#         form = CheckoutForm()
#         payment_method = PaymentMethodForm()
#         order = Order.objects.get(user = request.user, ordered=False)       
        
#         context = {
#             'form':form,
#             'payment_method':payment_method,
#             'order':order
#         }
#         return render(request, 'app_payment/checkout.html',context)

#     def post(self, request, *args, **kwargs):
#         form = CheckoutForm(request.POST)
#         payment_obj = Order.objects.get(user=request.user, ordered=False)
#         pay_form = PaymentMethodForm(request.POST, instance=payment_obj)
        
#         if form.is_valid() and pay_form.is_valid():
#             name = form.cleaned_data.get('name')
#             phone = form.cleaned_data.get('phone')
#             email = form.cleaned_data.get('email')
#             address = form.cleaned_data.get('address')
#             order_note = form.cleaned_data.get('order_note')

#             billing_address = Checkout(
#                 user=request.user,
#                 name=name,
#                 phone=phone,
#                 email=email,
#                 address=address,
#                 order_note=order_note
#             )
#             billing_address.save()
#             payment_obj.shipping_address = billing_address
#             pay_method = pay_form.save()

#             # Associating payment method with order
#             payment_obj.payment_option = pay_method

#             # Cash On Delivery
#             if pay_method == 'Cash on Delivery':
#                 order_items = Cart.objects.filter(user=request.user, purchased=False)
#                 for order_item in order_items:
#                     order_item.purchased = True
#                     order_item.save()

#                 payment_obj.ordered = True
#                 payment_obj.payment_option = pay_method.payment_option
#                 payment_obj.save()
                
#                 messages.success(request, "Your order was successful")
#                 return redirect('home')
#         return render(request, 'app_payment/checkout.html', {'form': form, 'payment_method': pay_form, 'order': payment_obj})


class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        form = CheckoutForm()
        payment_method = PaymentMethodForm()
        try:
            order = Order.objects.get(user=request.user, ordered=False)
        except Order.DoesNotExist:
            order = None
        
        context = {
            'form': form,
            'payment_method': payment_method,
            'order': order
        }
        return render(request, 'app_payment/checkout.html', context)

    def post(self, request, *args, **kwargs):
        form = CheckoutForm(request.POST)
        payment_form = PaymentMethodForm(request.POST)
        try:
            order = Order.objects.get(user=request.user, ordered=False)
        except Order.DoesNotExist:
            order = None

        if form.is_valid() and payment_form.is_valid() and order:
            name = form.cleaned_data.get('name')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            address = form.cleaned_data.get('address')
            order_note = form.cleaned_data.get('order_note')

            billing_address = Checkout.objects.create(
                user=request.user,
                name=name,
                phone=phone,
                email=email,
                address=address,
                order_note=order_note
            )
            order.shipping_address = billing_address

            # Save payment method
            payment_method = payment_form.cleaned_data.get('payment_option')
            order.payment_option = payment_method

            if payment_method == 'Cash On Delivery':
                # Mark items as purchased
                Cart.objects.filter(user=request.user, purchased=False).update(purchased=True)
                order.ordered = True
                order.save()
                messages.success(request, "Your order was successful")
                return redirect('home')
            elif payment_method == 'SSL Commerz':
                # Handle other payment methods (not implemented in this example)
                store_id = settings.STORE_ID
                store_pass = settings.STORE_PASS
                
                mypayment = SSLCSession(
                    sslc_is_sandbox=True,
                    sslc_store_id=store_id,
                    slc_store_pass=store_pass
                    )
                ###########--------------------#############
                status_url = request.build_absolute_uri(reverse('status'))
                mypayment.set_urls(
                    success_url=status_url,
                    fail_url=status_url, 
                    cancel_url=status_url, 
                    ipn_url=status_url
                    )
               ###################---------------------##################### 
                order_qs = Order.objects.filter(User=request.user, ordered=False)
                order_items = order_qs[0].orderitems.all()
                order_item_count = order_qs[0].order_items.count()
                order_total = order_qs[0].order_totals()
                
                mypayment.set_product_integration(
                    total_amount=Decimal(order_total),
                    currency='BDT',
                    product_category='clothing', 
                    product_name='demo-product', 
                    num_of_item=order_item_count, 
                    shipping_method='YES', 
                    product_profile='None')
        else:
            # Form validation failed
            messages.error(request, "Invalid form submission. Please check your inputs.")
        
        context = {
            'form': form,
            'payment_method': payment_form,
            'order': order
        }
        return render(request, 'app_payment/checkout.html', context)
    
    
@csrf_exempt
def sslc_status(request):
    if request.method == 'post' or request.method == 'POST':
        payment_data = request.POST
        status = payment_data['status']
        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']

            return HttpResponseRedirect(reverse('sslc-complete', kwargs={'val_id': val_id, 'tran_id': tran_id}))
    return render(request, 'index.html')

def sslc_complete(request, val_id, tran_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    order.ordered = True
    order.order_id = val_id
    order.payment_id = tran_id
    order.save()
    cart_items = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()
    messages.success(request, "You order was successful")
    return redirect('home')