from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    path = request.get_full_path()
    print(path)
    path = path.replace('/geostatus/post/?', '')
    path = path.split('&')
    lon = float(path[0].replace('lon=', ''))
    lat = float(path[1].replace('lat=', ''))
    return HttpResponse([lon, ' ', lat])
# Create your views here.
