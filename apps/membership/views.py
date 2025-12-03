from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.contrib.auth import get_user_model
from .models import Membership, MembershipType, MembershipHistory

User = get_user_model()


# -------------------------
# Список всех абонементов
# -------------------------
@login_required
def membership_list_view(request):
    types = MembershipType.objects.all()
    membership = getattr(request.user, "membership", None)

    return render(request, "membership/memberships.html", {
        "types": types,
        "current": membership,
    })


# -------------------------
# Покупка абонемента
# -------------------------
@login_required
def buy_membership_view(request, pk):
    user = request.user
    tariff = get_object_or_404(MembershipType, pk=pk)

    today = timezone.now().date()

    # EXISTING membership if user already purchased
    old_membership = getattr(user, "membership", None)

    # If active — extend
    if old_membership and old_membership.end_date >= today:
        old_membership.end_date = old_membership.end_date + timezone.timedelta(days=tariff.duration_days)
        old_membership.price += tariff.price
        old_membership.save()
    else:
        # Create or update membership
        Membership.objects.update_or_create(
            user=user,
            defaults={
                "type": tariff.name,
                "price": tariff.price,
                "start_date": today,
                "end_date": today + timezone.timedelta(days=tariff.duration_days),
                "frozen": False,
            }
        )

    # Save to history
    MembershipHistory.objects.create(
        user=user,
        membership_type=tariff.name,
        price=tariff.price,
        start_date=today,
        end_date=today + timezone.timedelta(days=tariff.duration_days)
    )

    return redirect("membership_success")


# -------------------------
# Страница успеха покупки
# -------------------------
@login_required
def membership_success_view(request):
    membership = getattr(request.user, "membership", None)
    return render(request, "membership/success.html", {
        "membership": membership
    })


# -------------------------
# История покупок абонементов
# -------------------------
@login_required
def membership_history_view(request):
    history = MembershipHistory.objects.filter(user=request.user).order_by("-purchased_at")

    return render(request, "membership/history.html", {
        "history": history
    })
