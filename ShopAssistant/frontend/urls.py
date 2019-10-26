from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.geoposition),
    path('signup/', views.index),
    path('post/', include('geolocation.urls')),
]
