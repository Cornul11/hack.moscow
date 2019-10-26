from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index),
    path('post/', include('geolocation.urls')),
]
