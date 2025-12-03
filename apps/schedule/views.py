from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import ClassSchedule
from apps.bookings.models import Booking
from apps.membership.models import Membership


@login_required
def schedule_view(request):
    today = timezone.now().date()

    classes = ClassSchedule.objects.filter(
        date__gte=today
    ).order_by("date", "time")

    return render(request, "schedule/schedule.html", {"classes": classes})

@login_required
def book_class(request, class_id):
    user = request.user
    schedule = get_object_or_404(ClassSchedule, id=class_id)

    # 1. Проверка абонемента
    membership = getattr(user, "membership", None)
    if not membership or not membership.is_active():
        return render(request, "schedule/error.html", {
            "message": "У вас нет активного абонемента"
        })

    # 2. Проверка что время тренировки не прошло
    if schedule.date < timezone.now().date():
        return render(request, "schedule/error.html", {
            "message": "Эта тренировка уже прошла"
        })

    # 3. Проверка что не записан уже
    if Booking.objects.filter(user=user, schedule=schedule).exists():
        return render(request, "schedule/error.html", {
            "message": "Вы уже записаны на это занятие"
        })

    # 4. Ограничение по количеству мест
    if Booking.objects.filter(schedule=schedule).count() >= schedule.max_clients:
        return render(request, "schedule/error.html", {
            "message": "Нет свободных мест"
        })

    # 5. Создание записи
    Booking.objects.create(user=user, schedule=schedule)

    # 6. Обновление статистики
    profile = user.client_profile
    profile.total_trainings += 1
    profile.monthly_trainings += 1
    profile.save()

    return redirect("profile")


@login_required
def cancel_booking(request, booking_id):
    user = request.user
    booking = get_object_or_404(Booking, id=booking_id, user=user)

    booking.delete()

    return redirect("profile")
