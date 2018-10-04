from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(RouteSchedule)
admin.site.register(Flight)
admin.site.register(Booking)
admin.site.register(Passenger)
