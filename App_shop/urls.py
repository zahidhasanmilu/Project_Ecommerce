from django.urls import path

from .import views


urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('product/details/<slug:slug>', views.ProductDetails.as_view(), name='product_details'),
    # path('product/details/<str:slug>', views.ProductDetails, name='product_details'),
    path('searchProduct/', views.searchProduct, name='searchProduct'),

]
