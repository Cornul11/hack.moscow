
from django.shortcuts import render
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import render, redirect
from database.models import Users, UsersInterests, Interests


def index(request):
    return render(request, 'login.html')

def geoposition(request):
    return render(request, 'collector.html'
                           '')




# Create your views here.

def recommendations(request):
    return render(request, 'recommendationsPage.html')

