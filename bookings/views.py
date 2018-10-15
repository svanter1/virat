from django.shortcuts import render
from django.http import HttpResponse
from .models import FlightInfo

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def home(request):
    flight = FlightInfo.objects.all()
    args = {'source': flight}

    if request.method == 'POST':
        src = request.POST['source']
        dest = request.POST['destination']
        count = request.POST['passengers']
        date = request.POST['date']

        #required_flights = flight.fliter(source = src)
        return HttpResponse(src+dest+count+date)

    else:
        return render(request, 'index.html', args)



def newpay(request):
    return render(request, 'newpay1.html')


'''def searchResults(request):
    flightInfo = FlightInfo.objects.all()
    flights = list()
    for flight in flightInfo:
        flights.append(flight.source)
    return HttpResponse(flights)'''