from django.urls import path

from App_payment import views


urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout')
]
