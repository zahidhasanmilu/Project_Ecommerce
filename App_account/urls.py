from django.urls import path

from .import views

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('signin/', views.user_signin, name='signin'),
    path('signout', views.user_signout, name='signout'),
]
