from django.shortcuts import render



def geoposition(request):
    return render(request, 'collector.html')
