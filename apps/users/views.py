from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone

from .forms import RegisterForm, ClientProfileForm
from .models import ClientProfile
from apps.membership.models import Membership
from apps.bookings.models import Booking


# -----------------------------
# LOGIN
# -----------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("index")
        else:
            return render(
                request,
                "users/auth.html",
                {"mode": "login", "error": "Неверный логин или пароль"}
            )

    return render(request, "users/auth.html", {"mode": "login"})


# -----------------------------
# REGISTER
# -----------------------------
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        else:
            return render(
                request,
                "users/auth.html",
                {"mode": "register", "form": form}
            )

    form = RegisterForm()
    return render(request, "users/auth.html", {"mode": "register", "form": form})


# -----------------------------
# LOGOUT
# -----------------------------
def logout_view(request):
    logout(request)
    return redirect("login")


# -----------------------------
# RESET PASSWORD
# -----------------------------
class ResetPasswordView(PasswordResetView):
    template_name = "users/reset_password.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("login")


# -----------------------------
# CABINET — ROLE BASED
# -----------------------------
@login_required
def cabinet_view(request):
    user = request.user

    if user.role == "trainer":
        return render(request, "users/cabinet_trainer.html")

    if user.role == "admin":
        return render(request, "users/cabinet_admin.html")

    # client
    profile = user.client_profile
    return render(request, "users/cabinet_client.html", {"profile": profile})


# -----------------------------
# FULL PROFILE PAGE (PREMIUM)
# -----------------------------
@login_required
def profile_view(request):
    user = request.user

    # профиль клиента
    profile = user.client_profile

    # абонемент (если есть)
    membership = getattr(user, "membership", None)

    # ближайшие записи (до 5)
    upcoming_bookings = Booking.objects.filter(
        user=user,
        schedule__date__gte=timezone.now().date()
    ).order_by("schedule__date", "schedule__time")[:5]

    # статистика
    stats = {
        "total_trainings": profile.total_trainings,
        "monthly_trainings": profile.monthly_trainings,
        "streak": profile.streak,
    }

    context = {
        "user": user,
        "profile": profile,
        "membership": membership,
        "upcoming_bookings": upcoming_bookings,
        "stats": stats
    }

    return render(request, "users/profile.html", context)


# -----------------------------
# EDIT PROFILE
# -----------------------------
@login_required
def profile_edit_view(request):
    profile = request.user.client_profile

    if request.method == "POST":
        form = ClientProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлён")
            return redirect("profile")
    else:
        form = ClientProfileForm(instance=profile)

    return render(request, "users/profile_edit.html", {"form": form})
