from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

from .forms import RegisterForm


# ---------------- LOGIN ---------------- #

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("index")   # <<< ПОСЛЕ ВХОДА — НА ГЛАВНУЮ
        else:
            return render(
                request,
                "users/auth.html",
                {"mode": "login", "error": "Неверные логин или пароль"}
            )

    return render(request, "users/auth.html", {"mode": "login"})


# ---------------- REGISTER ---------------- #

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")   # <<< ПОСЛЕ РЕГИСТРАЦИИ — НА ГЛАВНУЮ
        else:
            return render(
                request,
                "users/auth.html",
                {"mode": "register", "form": form}
            )

    form = RegisterForm()
    return render(request, "users/auth.html", {"mode": "register", "form": form})


# ---------------- LOGOUT ---------------- #

def logout_view(request):
    logout(request)
    return redirect("login")


# ---------------- RESET PASSWORD ---------------- #

class ResetPasswordView(PasswordResetView):
    template_name = "users/reset_password.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("login")


# ---------------- CABINET (ROLE-BASED) ---------------- #

@login_required
def cabinet_view(request):
    user = request.user


    if hasattr(user, "role"):

        if user.role == "trainer":
            return render(request, "users/cabinet_trainer.html")

        if user.role == "admin":
            return render(request, "users/cabinet_admin.html")

        # по умолчанию — клиент
        return render(request, "users/cabinet_client.html")

    # fallback — если нет роли
    return render(request, "users/cabinet_client.html")
