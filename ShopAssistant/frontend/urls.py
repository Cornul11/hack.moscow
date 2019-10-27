from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.geoposition),
    path('recommendations/', views.recommendations),
    path('search/', views.search),
    path('map/', views.map),
    path('signup/', views.index),
    path('post/', include('geolocation.urls')),

]
