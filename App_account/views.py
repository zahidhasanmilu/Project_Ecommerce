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
from .EmailBackEnd import EmailBackEnd

# forms
from App_account.forms import SignUpForm

# message
from django.contrib import messages

import uuid
from django.db.models import Q

# Create your views here.

def user_signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Additional processing if needed before saving to the database
            user.save()
            messages.success(request, "Login Successfully")
            return redirect('home')  # Redirect to a success page

    context = {
        'form': form
    }

    return render(request, 'app_account/signup.html', context)


def user_signin(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = EmailBackEnd.authenticate(
            request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successfully!')
            return redirect('home')
        else:
            messages.warning(request, 'Invalid email or password.')
            return redirect('signin')

    return render(request, 'app_account/signin.html')

@login_required
def user_signout(request):
    logout(request)
    messages.success(request, 'Loogout Succesful')
    return redirect('signin')
