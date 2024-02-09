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
from App_shop.models import Product, Category,ProductImage

# forms
from App_account.forms import SignUpForm

# message
from django.contrib import messages

import uuid
from django.db.models import Q
# Create your views here.


class HomeListView(ListView):
    model = Product
    template_name = 'app_shop/index.html'  # Your template file name
    context_object_name = 'products'  # Variable name used in the template
    ordering = ['-id']  # Optionally, specify the ordering of the queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        return context

class ProductDetails(DetailView):
    model = Product
    template_name = 'app_shop/product_details.html'  # Your template file name
    context_object_name = 'item'  # Variable name used in the template
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       # Fetch related data
        product_images = ProductImage.objects.filter(product=self.object.id)
        related_products = Product.objects.filter(category=self.object.category).exclude(pk=self.object.id)
        
        context["product_images"] = product_images
        context["related_products"] = related_products

        return context
    

# def ProductDetails(request, slug):
#     product_item = Product.objects.get(slug=slug)
#     product_images = ProductImage.objects.filter(product=product_item)
    
#     related_products = Product.objects.filter(Q(category = product_item.category)).exclude(pk = product_item.pk)
    
#     context={
#         'item':product_item,
#         'product_images':product_images,
#         'related_products':related_products
        
#     }
#     return render(request, 'app_shop/product_details.html',context )      


def searchProduct(request):  
    query = request.GET['q']
    product = Product.objects.filter(Q(name__icontains=query)|Q(category__name__icontains=query))
    context ={
        'product':product,
        'query':query
    }
    return render(request, 'app_shop/search_product.html',context)