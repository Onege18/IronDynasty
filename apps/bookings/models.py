from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Booking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    # Строковая ссылка — чтобы избежать циклического импорта
    schedule = models.ForeignKey(
        "schedule.ClassSchedule",
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Запись {self.user.username} на {self.schedule}"
