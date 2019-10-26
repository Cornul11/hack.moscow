import time
import requests
from geopy import distance
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from database.models import Shops, Users, UsersInterests
from django.contrib.sessions.backends.db import SessionStore

locationtracing = {}
# DEBUG = False
#
# if DEBUG:
#
# [[55.75561790448445, 37.61440535517105], [55.75561790448445, 37.61440535517105],
#                 [55.75589286291935, 37.61426535587848], [55.75589286291935, 37.61426535587848],
#                 [55.75635860211721, 37.614947788187344], [55.75635860211721, 37.614947788187344],
#                 [55.75635860211721, 37.614947788187344], [55.75599997035329, 37.61565567164093],
#                 [55.75599997035329, 37.61565567164093]]
# i = 0


@csrf_exempt
def index(request):
    if request.method == 'GET':
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
        request.session['user_imprint'] = response.json() if response else {}
        response = requests.post(url + 'recommendation', json=request.session['user_imprint'],
                                 headers={'content-type': 'application/json'})
        return JsonResponse(response.json() if response else {})
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


    if dist > 0.5:

        data = {
            'venue_id': 'DM_20518',
            'lat': lat,
            'lon': lon,
        }
        shop = requests.post(url + 'closest_shoppings', json=data,
                             headers={'content-type': 'application/json'})

        love_shop = shop.json() if response else None
        pop_location = locationtracing.pop(user.email)
        duration = time.time() - pop_location['start_time']
        if duration > 20:

            if love_shop:
                shop = Shops.objects.create(name=love_shop['items'][0], email=user,
                                            start_time=pop_location['start_time'],
                                            duration=duration)
                shop.save()

    return JsonResponse({})
# Create your views here.
