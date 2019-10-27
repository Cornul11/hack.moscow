from django.shortcuts import render
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import render, redirect
from database.models import Users, UsersInterests, Interests


def index(request):
    return render(request, 'login.html')


def geoposition(request):
    return render(request, 'collector.html'
                           '')


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
