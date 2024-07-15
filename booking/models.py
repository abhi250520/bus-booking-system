# booking/models.py

from django.db import models
from django.contrib.auth.models import User

class Bus(models.Model):
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    date_of_journey = models.DateField()
    start_time = models.TimeField()
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    stops = models.JSONField()

    def __str__(self):
        return f'{self.source} to {self.destination} on {self.date_of_journey}'

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    pickup_point = models.CharField(max_length=255)
    num_passengers = models.IntegerField()
    blocking_id = models.CharField(max_length=255, unique=True)
    booking_id = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} booking for {self.bus}'
