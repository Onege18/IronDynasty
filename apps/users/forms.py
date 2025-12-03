from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, ClientProfile


# ------------------------------
# Форма регистрации
# ------------------------------
class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ["username", "email", "role", "password1", "password2"]


# ------------------------------
# Форма редактирования профиля клиента
# ------------------------------
class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ["phone", "gender", "birth_date", "avatar"]

        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }
