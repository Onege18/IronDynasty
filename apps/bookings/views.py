from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Booking

@login_required
def my_bookings_view(request):
    user = request.user

    # ближайшие занятия
    upcoming = Booking.objects.filter(
        user=user,
        schedule__date__gte=timezone.now().date()
    ).order_by("schedule__date", "schedule__time")

    # прошедшие (для истории посещений)
    past = Booking.objects.filter(
        user=user,
        schedule__date__lt=timezone.now().date()
    ).order_by("-schedule__date", "-schedule__time")

    return render(request, "bookings/my_bookings.html", {
        "upcoming": upcoming,
        "past": past
    })
