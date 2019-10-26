from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('gologin', views.gologin),
    path('success', views.success),
    path('interests', views.interests),
]