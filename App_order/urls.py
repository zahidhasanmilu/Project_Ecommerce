from django.urls import path

from .import views


urlpatterns = [
    path('cart/<int:pk>/', views.add_to_cart, name='addtocart'),
    path('cart/summery/', views.cart_view, name='cart_view'),
    path('remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('card_increment/<int:pk>/', views.card_increment, name='card_increment'),
    path('card_decrement/<int:pk>/', views.card_decrement, name='card_decrement'),

]
