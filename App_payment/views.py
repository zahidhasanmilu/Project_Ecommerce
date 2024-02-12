from django.conf import settings
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect, HttpResponse
from django.urls import reverse, reverse_lazy

# VIEW
from django.views.generic import CreateView, ListView, DetailView, UpdateView, View, TemplateView, DeleteView

# Authentication
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt

# forms
from django.contrib.auth.forms import AuthenticationForm

# models
from App_account.models import User, Profile
from App_order.models import Order, Cart
from App_payment.models import Checkout

# forms
from App_account.forms import SignUpForm
from App_payment.forms import CheckoutForm, PaymentMethodForm

# message
from django.contrib import messages

import uuid
from django.db.models import Q

# for SSL COMMERZ
from decimal import Decimal
from sslcommerz_python.payment import SSLCSession

#Create view here
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
            order.save()  # Save the order after updating shipping address and payment option

            if payment_method == 'Cash On Delivery':
                # Mark items as purchased
                Cart.objects.filter(user=request.user,
                                    purchased=False).update(purchased=True)
                order.ordered = True
                order.save()  # Save the order after updating ordered status
                messages.success(request, "Your order was successful")
                return redirect('home')
            elif payment_method == 'SSL Commerzs':
                # Handle other payment methods (not implemented in this example)
                store_id = settings.STORE_ID
                store_pass = settings.STORE_PASS

                mypayment = SSLCSession(
                    sslc_is_sandbox=True,
                    sslc_store_id=store_id,
                    sslc_store_pass=store_pass
                )
                ########### --------------------#############
                status_url = request.build_absolute_uri(reverse('status'))
                mypayment.set_urls(
                    success_url=status_url,
                    fail_url=status_url,
                    cancel_url=status_url,
                    ipn_url=status_url
                )
               ################### ---------------------#####################
                order_qs = Order.objects.filter(user=request.user, ordered=False)
                order = order_qs.first()
                order_items = order.orderitems.all()
                # Use count() directly on order_items queryset
                order_item_count = order_items.count()
                order_total = order.order_totals()

                mypayment.set_product_integration(
                        total_amount=Decimal(order_total),
                        currency='BDT',
                        product_category='clothing',
                        product_name=order_items,
                        num_of_item=order_item_count,
                        shipping_method='YES',
                        product_profile='None'
                )

                current_user = request.user
                mypayment.set_customer_info(
                        name=current_user.user_name,
                        email=email,
                        address1=address,
                        city='Dhaka',
                        postcode='1207',
                        country='Bangladesh',
                        phone=phone
                )
                mypayment.set_shipping_info(
                        shipping_to=current_user.user_name,
                        address=address,
                        city='Dhaka',
                        postcode='1209',
                        country='Bangladesh'
                )
                response_data = mypayment.init_payment()
                print(response_data)
                return redirect(response_data['GatewayPageURL'])

        else:
            # Form validation failed
            messages.error(
                request, "Invalid form submission. Please check your inputs.")

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
