from django.urls import path
from .views import HomeView, SignupView, LoginView, logout_view, SearchBusesView, block_seats, book_tickets, BusListCreateAPIView, BookingCreateAPIView, BookTicketsAPIView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('search_buses/', SearchBusesView.as_view(), name='search_buses'),
    path('block_seats/<int:bus_id>/', block_seats, name='block_seats'),
    path('book_tickets/<str:blocking_id>/', book_tickets, name='book_tickets'),

    # API endpoints
    path('api/buses/', BusListCreateAPIView.as_view(), name='bus-list-create'),
    path('api/bookings/', BookingCreateAPIView.as_view(), name='booking-create'),
    path('api/book_tickets/', BookTicketsAPIView.as_view(), name='book-tickets'),
]
