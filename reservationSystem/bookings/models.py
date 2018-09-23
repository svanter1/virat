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
