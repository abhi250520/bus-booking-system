# booking/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Bus, Booking
from .serializers import BusSerializer, BookingSerializer
import json

# Frontend views
class HomeView(View):
    def get(self, request):
        return render(request, 'booking/home.html')

class SignupView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        return render(request, 'registration/signup.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

class SearchBusesView(View):
    def get(self, request):
        source = request.GET.get('source')
        destination = request.GET.get('destination')
        date_of_journey = request.GET.get('date_of_journey')
        if source and destination and date_of_journey:
            buses = Bus.objects.filter(source=source, destination=destination, date_of_journey=date_of_journey)
            return render(request, 'booking/search_buses.html', {'buses': buses})
        return render(request, 'booking/search_buses.html')

@login_required
def block_seats(request, bus_id):
    if request.method == 'POST':
        bus = Bus.objects.get(id=bus_id)
        pickup_point = request.POST.get('pickup_point')
        num_passengers = int(request.POST.get('num_passengers'))
        blocking_id = f"block_{bus_id}_{request.user.id}"
        Booking.objects.create(user=request.user, bus=bus, pickup_point=pickup_point, num_passengers=num_passengers, blocking_id=blocking_id)
        return redirect('book_tickets', blocking_id=blocking_id)
    return render(request, 'booking/block_seats.html', {'bus_id': bus_id})

@login_required
def book_tickets(request, blocking_id):
    if request.method == 'POST':
        booking = Booking.objects.get(blocking_id=blocking_id, user=request.user)
        booking_id = f"book_{booking.id}"
        booking.booking_id = booking_id
        booking.save()
        return render(request, 'booking/book_tickets.html', {'booking_id': booking_id})
    return render(request, 'booking/book_tickets.html', {'blocking_id': blocking_id})

# API views
class BusListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        source = request.query_params.get('source')
        destination = request.query_params.get('destination')
        date_of_journey = request.query_params.get('date_of_journey')
        if source and destination and date_of_journey:
            buses = Bus.objects.filter(source=source, destination=destination, date_of_journey=date_of_journey)
        else:
            buses = Bus.objects.all()
        serializer = BusSerializer(buses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookTicketsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        blocking_id = request.data.get('blocking_id')
        booking = Booking.objects.get(blocking_id=blocking_id, user=request.user)
        booking_id = f"book_{booking.id}"
        booking.booking_id = booking_id
        booking.save()
        return Response({'booking_id': booking_id}, status=status.HTTP_200_OK)
