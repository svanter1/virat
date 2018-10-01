from django.db import models


class RouteSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    layover = models.IntegerField()
    depature = models.TimeField()
    arrival = models.TimeField()
    duration = models.DurationField()


class Flight(models.Model):
    id = models.AutoField(primary_key=True)
    flight_model = models.IntegerField(unique=True)
    routes = models.ForeignKey(RouteSchedule, on_delete=models.CASCADE)

    
class Booking(models.Model):
    bid = models.AutoField(primary_key=True)
    flight = models.ForeignKey(Flight, default=None, on_delete=models.CASCADE)
    route = models.ForeignKey(RouteSchedule, default=None, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    travel_class = models.CharField(max_length=3)

class Passenger(models.Model):
    pid = models.AutoField(primary_key = True)
    booking_id = models.ForeignKey(Booking, default=None, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField()
    sex = models.CharField(max_length=1)
    passport = models.CharField(max_length=10)
    seat_no = models.CharField(max_length=3)
