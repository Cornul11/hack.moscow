from django.shortcuts import render
from django.http import HttpResponse



def index(request):
    lon = request.POST['lon']
    lat = request.POST['lat']
    return HttpResponse(lon)
# Create your views here.
