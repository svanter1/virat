from django.shortcuts import render
from django.http import HttpResponse
from .models import FlightInfo


def home(request):
    return render(request, 'index.html')
def newpay(request):
    return render(request, 'newpay1.html')

def searchResults(request):
    flightInfo = FlightInfo.objects.all()
    flights = list()
    for flight in flightInfo:
        flights.append(flight.source)
    return HttpResponse(flights)