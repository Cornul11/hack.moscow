import time
from geopy import distance
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from database.models import Shops, Users
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
    print(locationtracing.get(user.email))
    if not locationtracing.get(user.email):
        locationtracing[user.email] = {'lon': lon, 'lat': lat,
                                       'start_time': time.time(), 'name': str(lat) + str(lon)}
    dist = distance.geodesic((lat, lon), (
                    locationtracing[user.email]['lat'], locationtracing[user.email]['lon'])).m
    print(dist)
    if dist > 15:
        pop_location = locationtracing.pop(user.email)
        duration = time.time() - pop_location['time']
        if duration > 300:
            shop = Shops.objects.create(name=pop_location['name'], email=user,
                                        start_time=pop_location[start_time], duration=duration)
            shop.save()

    return HttpResponse(locationtracing[request.session['email']])
# Create your views here.
