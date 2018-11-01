from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import FlightInfo, FlightDetails
import datetime
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    flight = FlightInfo.objects.values('source', 'destination').distinct()
    args = {'source': flight}

    if request.method == 'POST':
        src = request.POST['source']
        dest = request.POST['destination']
        count = request.POST['passengers']
        date = request.POST['date']
        cls = request.POST['clss']

        request.session['depature_date'] = date
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

                        request.session['bseats'] = count
                    else:
                        trn = FlightDetails.objects.filter(flight_id=flt.flight_id, available_eseats__gte=count,
                                                           departure_date=date)
                        request.session['eseats'] = count
                    if trn:
                        args['details'] += [[flt.source, flt.destination, date, flt.departure, flt.arrival,
                                             flt.duration_hrs, flt.price, flt.flight_id, count]]

        return render(request, 'searchResults.html', args)

    else:
        return render(request, 'index.html', args)

@csrf_exempt
def passenger(request):
    flight_id = request.GET.get('flt_id')
    pass_count = request.GET.get('cnt')
    if request.method == 'POST':
        first_name = request.POST['name']
        last_name = request.POST['lastname']
        passport = request.POST['pass']
        gender = request.POST['gender']
        age = request.POST['age']

        request.session['flight_id'] = flight_id
        request.session['firstname'] = first_name
        request.session['lastname'] = last_name
        request.session['passport'] = passport
        request.session['gender'] = gender
        request.session['age'] = age

        if request.POST['option'] == "Continue":
            return newpay(request)
        else:
            return redirect('home')
    else:
        return render(request, 'passengers.html')

@csrf_exempt
def newpay(request):
    if request.method == 'POST':
        return render(request, 'payment.html')


def reservation(request):
    return render(request, 'reservationStatus.html')
