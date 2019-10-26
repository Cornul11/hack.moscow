import time
import requests
from geopy import distance
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from database.models import Shops, Users, UsersInterests
from django.contrib.sessions.backends.db import SessionStore

locationtracing = {}


@csrf_exempt
def index(request):
    path = request.get_full_path()

    path = path.replace('/geostatus/post/?', '')
    path = path.split('&')
    lon = float(path[0].replace('lon=', ''))
    lat = float(path[1].replace('lat=', ''))
    s = SessionStore()
    user = Users.objects.filter(email=request.session['email']).first()
    if not locationtracing.get(user.email):
        locationtracing[user.email] = {'lon': lon, 'lat': lat,
                                       'start_time': time.time(), 'name': str(lat) + str(lon)}
    dist = distance.geodesic((lat, lon), (
                    locationtracing[user.email]['lat'], locationtracing[user.email]['lon'])).m
    content = []
    for i in UsersInterests.objects.filter(email=request.session['email']):
        content.append(i.interest.name)

    fav_shops = []
    for i in Shops.objects.filter(email=request.session['email']):
        if not i.start:
            continue
        fav_shops.append(i.start)

    url = 'https://f785bb17.ngrok.io/'
    data = {
        'content': content,
        'fav_shops': fav_shops,
    }
    response = requests.post(url + 'user_imprint', json=data,
                             headers={'content-type': 'application/json'})
    request.session['user_imprint'] = response.json()
    response = requests.post(url + 'recommendation', json=request.session['user_imprint'],
                             headers={'content-type': 'application/json'})

    if dist > 15:
        pop_location = locationtracing.pop(user.email)
        duration = time.time() - pop_location['start_time']
        if duration > 300:

            shop = Shops.objects.create(name=pop_location['name'], email=user,
                                        start_time=pop_location['start_time'], duration=duration)

            shop.save()

    return JsonResponse(response.json())
# Create your views here.
