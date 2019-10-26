from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

locationtracing = {}


@csrf_exempt
def index(request):
    path = request.get_full_path()
    print(path)
    path = path.replace('/geostatus/post/?', '')
    path = path.split('&')
    lon = float(path[0].replace('lon=', ''))
    lat = float(path[1].replace('lat=', ''))
    print(locationtracing.get(request.session['email']))
    if not locationtracing.get(request.session['email']):
        locationtracing[request.session['email']] = {'lon': lon, 'lat': lat, 'count': 1}
    else:
        locationtracing[request.session['email']]['count']+=1

    return HttpResponse(locationtracing[request.session['email']])
# Create your views here.
