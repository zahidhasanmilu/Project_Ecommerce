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
# from sslcommerz_python.payment import SSLCSession
# from decimal import Decimal

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
                pass
        else:
            # Form validation failed
            messages.error(request, "Invalid form submission. Please check your inputs.")
        
        context = {
            'form': form,
            'payment_method': payment_form,
            'order': order
        }
        return render(request, 'app_payment/checkout.html', context)