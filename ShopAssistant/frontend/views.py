import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import render, redirect
from database.models import Users, UsersInterests, Interests
import requests
from django.http import JsonResponse


def index(request):
    return render(request, 'login.html')


def map(request):
    lat = request.GET['lat']
    lon = request.GET['lon']
    originalLat = request.GET['x']
    originalLon = request.GET['y']
    print(lat, lon, originalLat, originalLon)
    return render(request, 'map.html')


def geoposition(request):
    return render(request, 'collector.html')


def search(request):
    if request.method == "GET":
        url = 'https://7ee50b98.ngrok.io/search'
        data = {
            'user_imprint': request.session['user_imprint'].get('user_imprint', []),
            'request': request.GET.get('search', ''),
        }
        response = requests.post(url, json=data, headers={'Content-type': 'application/json'})
        request.session['search'] = data['request']
        request.session['search_response'] = response.json() if response else {}
        return redirect('/geostatus/recommendations/')

# Create your views here.

def recommendations(request):
    return render(request, 'recommendationsPage.html')
