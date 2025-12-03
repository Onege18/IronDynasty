from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="trainer_profile")

    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    specialization = models.CharField(max_length=100, blank=True)

    photo = models.ImageField(upload_to="trainers/", null=True, blank=True)

    experience_years = models.IntegerField(default=0)

    def __str__(self):
        return self.name
