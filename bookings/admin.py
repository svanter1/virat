from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(FlightInfo)
admin.site.register(FlightDetails)
admin.site.register(CustomerInfo)
admin.site.register(BookingInfo)
