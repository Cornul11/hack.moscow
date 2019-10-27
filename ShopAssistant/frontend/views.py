import requests
from django.http import JsonResponse
from django.shortcuts import render


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
        url = 'https://e5d6c151.ngrok.io/search'
        data = {
            'user_imprint': request.session['user_imprint'],
            'request': request.GET['text'],
        }
        response = requests.post(url, json=data,
                                 headers={'Content-type': 'application/json'})
        return JsonResponse(response.json() if response else {})


# Create your views here.

def recommendations(request):
    return render(request, 'recommendationsPage.html')
