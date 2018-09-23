from django.db import models
# Create your models here.


class Flight(models.Model):
    id = models.AutoField(primary_key=True)
    flight_model = models.IntegerField(max_length=10, unique=True)
    routes = models.ForeignKey(RouteSchedule, on_delete=models.CASCADE)


class RouteSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    layover = models.IntegerField()
    depature = models.TimeField()
    arrival = models.TimeField()
    duration = models.DurationField()