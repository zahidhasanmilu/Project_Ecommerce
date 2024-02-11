from django.urls import path

from App_payment import views


urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path("sslc/statuse/", views.sslc_status, name="status"),
    path("sslc/complete/<val_id>/<tran_id>/", views.sslc_complete, name="sslc-complete"),
]
