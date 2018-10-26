from django.shortcuts import render
from django.http import HttpResponse
from .models import FlightInfo, FlightDetails
import datetime

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def home(request):
    #flight = FlightInfo.objects.all()
    flight = FlightInfo.objects.values('source', 'destination').distinct()
    args = {'source': flight}

    if request.method == 'POST':
        src = request.POST['source']
        dest = request.POST['destination']
        count = request.POST['passengers']
        date = request.POST['date']
        cls = request.POST['class']

        required_flights = FlightInfo.objects.filter(source=src, destination=dest)
        args['details'] = []

        if date >= datetime.datetime.today().strftime('%Y-%m-%d'):
            for flt in required_flights:
                date_trn = FlightDetails.objects.filter(flight_id=flt.flight_id, departure_date=date)

                if not date_trn:
                    args['details'] += [[flt.source, flt.destination, date, flt.departure, flt.arrival,
                                         flt.duration_hrs, flt.price, flt.flight_id, count]]

                else:
                    if cls:
                        trn = FlightDetails.objects.filter(flight_id=flt.flight_id, available_bseats__gte=count,
                                                       departure_date=date)
                    else:
                        trn = FlightDetails.objects.filter(flight_id=flt.flight_id, available_eseats__gte=count,
                                                       departure_date=date)

                    if trn:
                        args['details'] += [[flt.source, flt.destination, date, flt.departure, flt.arrival,
                                         flt.duration_hrs, flt.price, flt.flight_id, count]]

        return render(request, 'searchResults.html', args)

    else:
        return render(request, 'index.html', args)


def passenger(request):
    return render(request, 'passenger-details.html')

def newpay(request):
    return render(request, 'newpay1.html')


'''def searchResults(request):
    flightInfo = FlightInfo.objects.all()
    flights = list()
    for flight in flightInfo:
        flights.append(flight.source)
    return HttpResponse(flights)'''