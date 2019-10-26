from django.shortcuts import render


def index(request):
    return render(request, 'signup.html')


def geoposition(request):
    return render(request, 'collector.html')
