from django.db import models
from apps.trainers.models import Trainer


class ClassSchedule(models.Model):
    CLASS_TYPES = [
        ("yoga", "Йога"),
        ("boxing", "Бокс"),
        ("crossfit", "Кроссфит"),
        ("hiit", "HIIT"),
        ("strength", "Силовая"),
        ("personal", "Персональная тренировка"),
    ]

    class_name = models.CharField(max_length=50, choices=CLASS_TYPES)

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name="classes"
    )

    date = models.DateField()
    time = models.TimeField()

    max_clients = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.get_class_name_display()} — {self.date} {self.time}"
