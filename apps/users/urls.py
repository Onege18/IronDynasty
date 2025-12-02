from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    register_view, login_view, logout_view,
    ResetPasswordView, cabinet_view
)

urlpatterns = [

    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),


    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),


    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),


    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),


    path("cabinet/", cabinet_view, name="cabinet"),
]
