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
from App_shop.models import Product, Category, ProductImage
from App_order.models import Cart, Order

# forms
from App_account.forms import SignUpForm

# message
from django.contrib import messages

import uuid
from django.db.models import Q


# Create your views here.
@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(
        item=item, user=request.user, purchased=False)
    order_queryset = Order.objects.filter(user=request.user, ordered=False)

    if order_queryset.exists():
        order = order_queryset[0]
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.success(request, 'this item update succesfully')
            return redirect('product_details', slug=item.slug)
        else:
            order.orderitems.add(order_item[0])
            messages.success(request, 'this item added succesfully')
            return redirect('product_details', slug=item.slug)

    else:
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.success(request, 'this item update succesfully')
        return redirect('product_details', slug=item.slug)

@login_required
def card_increment(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item,created = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)    
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.orderitems.filter(item=item).exists():
            if not created:  # If the item was not just created
                order_item.quantity += 2
                order_item.save()
                messages.success(request, 'This product quantity updated')
                return redirect('cart_view')

    # If the order does not exist or the product is not in the order
    messages.warning(request, 'This product is not in your cart')
    return redirect('home')

@login_required
def card_decrement(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        order_item = order.orderitems.filter(item=item).first()

        if order_item:
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, 'This product quantity updated')
            else:
                # If the quantity is 1, remove the item from the cart
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.info(request, 'This product removed from your cart')
            return redirect('cart_view')

    # If the order does not exist or the product is not in the order
    messages.warning(request, 'This product is not in your cart')
    return redirect('home')


@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)

    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'app_order/cart_summery.html', {'carts': carts, 'order': order})
    else:
        messages.warning(request, 'You dont have item in your cart !!')
        return redirect("home")



@login_required
def remove_from_cart(request, pk):
    try:
        item = get_object_or_404(Product, pk=pk)
        order_queryset = Order.objects.filter(user=request.user, ordered=False)

        if order_queryset.exists():
            order = order_queryset[0]
            order_item = order.orderitems.filter(item=item).first()

            if order_item:
                # Assuming `Cart` is the model representing the cart items
                cart_item = get_object_or_404(
                    Cart, item=item, user=request.user, purchased=False)

                order.orderitems.remove(cart_item)
                cart_item.delete()

                messages.success(
                    request, 'This item has been removed successfully')
                return redirect('cart_view')
            else:
                messages.warning(request, 'This item is not in your cart')
                return redirect('home')
        else:
            messages.warning(request, 'You do not have an active order')
            return redirect('home')
    except Product.DoesNotExist:
        messages.warning(request, 'Product not found')
        return redirect('home')
