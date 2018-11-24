from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import FlightInfo, FlightDetails, BookingInfo, CustomerInfo
import datetime
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    request.session['flag'] = 'false'
    flight = FlightInfo.objects.values('source', 'destination').distinct()
    args = {'source': flight}

    if request.method == 'POST':
        src = request.POST['source']
        dest = request.POST['destination']
        count = request.POST['passengers']
        date = request.POST['date']
        cls = request.POST['clss']

        request.session['depature_date'] = date
        request.session['source'] = src
        request.session['destination'] = dest
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
        request.session['flag'] = 'true'

        return render(request, 'searchResults.html', args)

    else:
        request.session['flag'] = 'false'
        return render(request, 'index.html', args)

@csrf_exempt
def passenger(request):
    #print(request.session['flag'])
    try:
        if request.session['flag'] == 'true':
            #request.session['flag'] = 'false'
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
                request.session['tprice'] = int(pass_count) * int(price)

                if request.POST.get('option') == "Continue":
                    #request.session['flag'] = 'true'
                    return redirect('newpay')
                else:
                    request.session['flag'] = 'false'
                    return redirect('home')

            else:
                #request.session['flag'] = 'false'
                return render(request, 'passengers.html')
        else:
            #request.session['flag'] = 'false'
            return render(request, 'error_page.html')
    except:
        request.session['flag'] = 'false'
        return render(request, 'error_page.html')

@csrf_exempt
def newpay(request):
    try:
        if request.session['flag'] == 'true':
            if request.method == 'POST':
                if request.POST['p_option'] == "CANCEL":
                    return redirect('home')
                else:
                    custiterator = CustomerInfo.objects.all()
                    maxid = 0
                    for o in custiterator:
                        if o.customer_id > maxid:
                            maxid = o.customer_id
                    id = maxid + 1

                    cust = CustomerInfo(customer_id=id, first_name=request.session['firstname'], last_name=
                    request.session['lastname'], age=request.session['age'],
                                        gender=request.session['gender'], passport=request.session['passport'])
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
                    bidstr = str(id) + splittedtime[1] + splittedtime[2][:2]
                    bid = int(bidstr)
                    request.session['confirmationId'] = 'VA' + bidstr
                    flight_obj = FlightInfo.objects.get(flight_id=request.session['flight_id'])
                    booking = BookingInfo(booking_id=bid, customer=cust, flight=flight_obj,
                                          departure_date=request.session['depature_date'], status='Confirmed',
                                          seats=int(request.session['passenger_count']))
                    booking.save()
                    """import random
                    x = random.randint(1001, 9999)
                    request.session['confirmationId'] = 'VA'+str(x)"""
                    # print('Travel class:'+request.session['class'])
                    travelclass = int(request.session['class'])

                    mmddyyyy = request.session['depature_date'].split('-')
                    idsearch = request.session['flight_id']+str(mmddyyyy[1])+str(mmddyyyy[2])
                    #for s in mmddyyyy:
                     #   idsearch += s
                    fdid = int(idsearch)
                    try:
                        flightd = FlightDetails.objects.get(id=fdid)
                        if travelclass:
                            seatsc = flightd.available_bseats - int(request.session['passenger_count'])
                            fd2 = FlightDetails(flight=flight_obj, departure_date=request.session['depature_date'],
                                                available_bseats=seatsc,
                                                available_eseats=flightd.available_eseats, id=flightd.id)
                            fd2.save()
                        else:
                            seatsc = flightd.available_eseats - int(request.session['passenger_count'])
                            fd2 = FlightDetails(flight=flight_obj, departure_date=request.session['depature_date'],
                                                available_bseats=flightd.available_bseats,
                                                available_eseats=seatsc, id=flightd.id)
                            fd2.save()
                    except FlightDetails.DoesNotExist:
                        if travelclass:
                            seatsc = 10 - int(request.session['passenger_count'])
                            fd2 = FlightDetails(flight=flight_obj, departure_date=request.session['depature_date'],
                                                available_bseats=seatsc,
                                                available_eseats=30, id=fdid)
                            fd2.save()
                        else:
                            seatsc = 30 - int(request.session['passenger_count'])
                            fd2 = FlightDetails(flight=flight_obj, departure_date=request.session['depature_date'],
                                                available_bseats=10,
                                                available_eseats=seatsc, id=fdid)
                            fd2.save()
                        #fd1 = FlightDetails(flight=flight_obj, departure_date=request.session['depature_date'],
                         #                   available_bseats=10, available_eseats=30, id=fdid)
                        #fd1.save()

                    # flt_detail = FlightDetails()
                    request.session['flag'] = 'false'
                    return render(request, 'payment_success.html')
            else:
                return render(request, 'payment_new.html')
        else:
            #request.session['flag'] = 'false'
            return render(request, 'error_page.html')
    except:
        request.session['flag'] = 'false'
        return render(request, 'error_page.html')

def paymentsuccess(request):
    try:
        return render(request, 'payment_success.html')

    except:
        request.session['flag'] = 'false'
        return render(request, 'error_page.html')

@csrf_exempt
def reservation(request):

    if request.method == 'POST':

        try:
            booking_id = request.POST['bookid']
            book_args = {'book_id': booking_id}
            booking = BookingInfo.objects.values('flight_id', 'departure_date', 'status', 'seats')\
                .filter(booking_id=booking_id)

            if booking:
                for bok in booking:
                    book_args['fght_id'] = bok['flight_id']
                    book_args['depature_date'] = bok['departure_date']
                    book_args['status'] = bok['status']
                    book_args['seats'] = int(bok['seats'])

                    for flight in FlightInfo.objects.filter(flight_id=book_args['fght_id']):
                        book_args['depature_time'] = flight.departure
                        book_args['total_price'] = book_args['seats'] * int(flight.price)
                        book_args['source'] = flight.source
                        book_args['destination'] = flight.destination

                    request.session['c_source'] = book_args['source']
                    request.session['c_destination'] = book_args['destination']
                    request.session['cancel_book_id'] = booking_id
                    request.session['cancelled_seats'] = bok['seats']
                    request.session['cflight_id'] = bok['flight_id']

                    return render(request, 'flightDetails.html', book_args)
            else:
                return render(request, 'reservationNoValue.html')

        except:
            return render(request, 'reservationNoValue.html')

    else:
        if request.POST.get('option') == "Cancel+Reservation":
            return render(request, 'reservationNoValue.html')

        return render(request, 'reservationStatus.html')

@csrf_exempt
def cancellation(request):
    if request.method == 'POST':
        bid = int(request.session['cancel_book_id'])
        dt = int(str(bid)[-4:])
        cid = int(str(bid)[:-4])
        fdid = int(str(request.session['cflight_id'])+str(dt))
        BookingInfo.objects.filter(booking_id=bid).delete()
        CustomerInfo.objects.filter(customer_id=cid).delete()
        flight_obj = FlightInfo.objects.get(flight_id=request.session['cflight_id'])
        flightd = FlightDetails.objects.get(id=fdid)
        seatsc = flightd.available_eseats + int(request.session['cancelled_seats'])
        fd2 = FlightDetails(flight=flight_obj, departure_date=flightd.departure_date,
                            available_bseats=flightd.available_bseats,
                            available_eseats=seatsc, id=flightd.id)
        fd2.save()

        return render(request, 'cancellationSuccess.html')
    else:
        return render(request, 'error_page.html')


def about(request):
    return render(request, 'aboutUs.html')


def contact(request):
    return render(request, 'contactUs.html')
