from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()

class Membership(models.Model):

    # Варианты абонементов
    TYPE_CHOICES = [
        ("monthly", "Месячный"),
        ("quarter", "3 месяца"),
        ("year", "Годовой"),
        ("once", "Разовый"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="membership")

    # тип абонемента — удобно хранить в виде кода
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    # цена абонемента
    price = models.IntegerField(default=0)

    # даты абонемента
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()

    # статус заморозки
    frozen = models.BooleanField(default=False)
    frozen_at = models.DateField(null=True, blank=True)

    # -----------------------------------------
    # Методы абонемента
    # -----------------------------------------

    def is_active(self):
        """Активен ли абонемент?"""
        return self.end_date >= timezone.now().date() and not self.frozen

    def status(self):
        """Текстовый статус"""
        if self.frozen:
            return "Заморожен"
        if self.end_date < timezone.now().date():
            return "Истёк"
        return "Активен"

    def days_left(self):
        """Сколько дней осталось"""
        if self.end_date < timezone.now().date():
            return 0
        return (self.end_date - timezone.now().date()).days

    def freeze(self):
        """Заморозить абонемент"""
        if not self.frozen:
            self.frozen = True
            self.frozen_at = timezone.now().date()
            self.save()

    def unfreeze(self):
        """Разморозить абонемент (добавляем дни заморозки)"""
        if self.frozen:
            freeze_days = (timezone.now().date() - self.frozen_at).days
            self.end_date += timedelta(days=freeze_days)
            self.frozen = False
            self.frozen_at = None
            self.save()

    def duration_days(self):
        """Сколько всего дней длился абонемент"""
        return (self.end_date - self.start_date).days

    def __str__(self):
        return f"{self.get_type_display()} — {self.user.username}"

class MembershipType(models.Model):
    name = models.CharField(max_length=50)       # "Месячный", "Годовой"
    duration_days = models.IntegerField(default=30)
    price = models.IntegerField()

    def __str__(self):
        return self.name

class MembershipHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    membership_type = models.CharField(max_length=100)
    price = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.membership_type}"
