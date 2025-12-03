from django.contrib.auth.models import AbstractUser
from django.db import models


# -----------------------------
# CUSTOM USER MODEL
# -----------------------------
class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('trainer', 'Trainer'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='client'
    )

    def is_client(self):
        return self.role == 'client'

    def is_trainer(self):
        return self.role == 'trainer'

    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return f"{self.username} ({self.role})"


# -----------------------------
# CLIENT PROFILE MODEL
# -----------------------------

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class ClientProfile(models.Model):
    """
    Профиль клиента фитнес-клуба.

    Содержит персональные данные, статистику тренировок,
    аватар и связь с пользователем. Это расширение модели User.
    """

    # связь 1 к 1 с кастомным User
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="client_profile"
    )

    # --------------------------------------
    # ПЕРСОНАЛЬНАЯ ИНФОРМАЦИЯ
    # --------------------------------------
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Телефон клиента"
    )

    gender = models.CharField(
        max_length=10,
        choices=[
            ("female", "Женский"),
            ("male", "Мужской"),
            ("other", "Другое")
        ],
        blank=True,
        help_text="Пол клиента"
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
        help_text="Дата рождения клиента"
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
        help_text="Фото профиля"
    )

    # --------------------------------------
    # СТАТИСТИКА И ПРОГРЕСС
    # --------------------------------------
    total_trainings = models.PositiveIntegerField(
        default=0,
        help_text="Всего тренировок за весь период"
    )

    monthly_trainings = models.PositiveIntegerField(
        default=0,
        help_text="Тренировок за текущий месяц"
    )

    streak = models.PositiveIntegerField(
        default=0,
        help_text="Серия тренировки (сколько дней подряд клиент посещает занятия)"
    )

    # --------------------------------------
    # СИСТЕМНЫЕ ПОЛЯ
    # --------------------------------------
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Дата создания профиля"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Дата последнего обновления профиля"
    )

    # --------------------------------------
    # МЕТОДЫ УДОБСТВА
    # --------------------------------------

    def get_full_name(self):
        """Возвращает имя + фамилию, если заполнены, иначе username."""
        if self.user.first_name or self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}".strip()
        return self.user.username

    def age(self):
        """Возраст клиента (если указана дата рождения)."""
        if not self.birth_date:
            return None
        today = timezone.now().date()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    def __str__(self):
        return f"Профиль клиента: {self.user.username}"
