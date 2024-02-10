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
from App_order.models import Order

# forms
from App_account.forms import SignUpForm
from App_payment.forms import BillingAddressForm,PaymentMethodForm

# message
from django.contrib import messages

import uuid
from django.db.models import Q

# Create your views here.

class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        form = BillingAddressForm()
        payment_method = PaymentMethodForm()
        order = Order.objects.get(user = request.user, ordered=False)
        
        
        context = {
            'form':form,
            'payment_method':payment_method,
            'order':order
        }
        return render(request, 'app_payment/checkout.html',context)

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')