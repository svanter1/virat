from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import FlightInfo, FlightDetails

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

        required_flights = FlightInfo.objects.filter(source=src, destination=dest)
        args['details'] = []
        for flt in required_flights:
            date_trn = FlightDetails.objects.filter(flight_id=flt.flight_id, departure_date=date)
            trn = FlightDetails.objects.filter(flight_id=flt.flight_id, available_eseats__gte=count, departure_date=date)

            if not date_trn:
                args['details'] += [[flt.source, flt.destination, flt.departure, flt.arrival,
                                     flt.duration_hrs, flt.price]]

            elif trn:
                args['details'] += [[flt.source, flt.destination, flt.departure, flt.arrival,
                                     flt.duration_hrs, flt.price]]

        return render(request, 'searchResults.html', args)

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