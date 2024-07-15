from django.contrib import admin

# Register your models here.
from .models import Bus,  Booking #, Route, SearchHistory, BookingHistory


admin.site.register(Bus)
#admin.site.register(Route)
admin.site.register(Booking)
#admin.site.register(SearchHistory)
#admin.site.register(BookingHistory)
