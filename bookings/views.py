from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import FlightInfo, FlightDetails, BookingInfo, CustomerInfo
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
        request.session['class'] = cls
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
    price = request.GET.get('price')
    if request.method == 'POST':
        first_name = request.POST.get('name')
        last_name = request.POST.get('lastname')
        passport = request.POST.get('pass')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        request.session['flight_id'] = flight_id
        request.session['passenger_count'] = pass_count
        request.session['firstname'] = first_name
        request.session['lastname'] = last_name
        request.session['passport'] = passport
        request.session['gender'] = gender
        request.session['age'] = age
        request.session['tprice'] = int(pass_count)*int(price)

        if request.POST.get('option') == "Continue":
            return redirect('newpay')
        else:
            return redirect('home')

    else:
        return render(request, 'passengers.html')

@csrf_exempt
def newpay(request):
    if request.method == 'POST':
        if request.POST['p_option'] == "CANCEL":
            return redirect('home')
        else:
            custiterator = CustomerInfo.objects.all()
            maxid = 0
            for o in custiterator:
                if o.customer_id > maxid:
                    maxid = o.customer_id
            id = maxid+1

            cust = CustomerInfo(customer_id = id, first_name = request.session['firstname'], last_name =
                            request.session['lastname'], age = request.session['age'],
                                gender = request.session['gender'], passport = request.session['passport'])
            cust.save()
            """
            maxid = 0
            bookiterator = BookingInfo.objects.all()
            for o in bookiterator:
                if o.booking_id > maxid:
                    maxid = o.booking_id
            bid = maxid+1
            
            if(request.session['bseats'] == None):
                seats = request.session['bseats']
            else:
                seats = request.session['eseats']
            """
            import datetime
            timestr = str(datetime.datetime.now())
            splittedtime = timestr.split("-")
            bidstr = str(id)+splittedtime[1]+splittedtime[2][:2]
            bid = int(bidstr)
            request.session['confirmationId'] = 'VA'+bidstr
            flight_obj = FlightInfo.objects.get(flight_id=request.session['flight_id'])

            booking = BookingInfo(booking_id = bid, customer = cust, flight = flight_obj,
                                  departure_date = request.session['depature_date'], status = 'Confirmed',
                                  seats = 1)
            booking.save()
            """import random
            x = random.randint(1001, 9999)
            request.session['confirmationId'] = 'VA'+str(x)"""
            #print('Travel class:'+request.session['class'])
            travelclass = int(request.session['class'])

            mmddyyyy = request.session['depature_date'].split('-')
            idsearch = request.session['flight_id']
            for s in mmddyyyy:
                    idsearch += s
            fdid = int(idsearch)
            try:
                flightd = FlightDetails.objects.get(id=fdid)
                if travelclass:
                    seatsc = flightd.available_bseats - 1
                    fd2 = FlightDetails(flight=flight_obj, departure_date=request.session['depature_date'],
                                    available_bseats=seatsc,
                                    available_eseats=flightd.available_eseats, id=flightd.id)
                    fd2.save()
                else:
                    seatsc = flightd.available_eseats - 1
                    fd2 = FlightDetails(flight=flight_obj, departure_date=request.session['depature_date'],
                                    available_bseats=flightd.available_bseats,
                                    available_eseats=seatsc, id=flightd.id)
                    fd2.save()
            except FlightDetails.DoesNotExist:
                fd1 = FlightDetails(flight=flight_obj, departure_date=request.session['depature_date'],
                                    available_bseats=10, available_eseats=30, id=fdid)
                fd1.save()


            #flt_detail = FlightDetails()
            return render(request, 'payment_success.html')
    else:
        return render(request, 'payment_new.html')

def paymentsuccess(request):
    return render(request,'payment_success.html')


def reservation(request):
    return render(request, 'reservationStatus.html')
