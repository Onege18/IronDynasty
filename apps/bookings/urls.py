from django.urls import path
from .views import my_bookings_view

urlpatterns = [
    path('', my_bookings_view, name='my_bookings'),
]
