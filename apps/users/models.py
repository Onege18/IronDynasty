from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('trainer', 'Trainer'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

    def is_client(self):
        return self.role == 'client'

    def is_trainer(self):
        return self.role == 'trainer'

    def is_admin(self):
        return self.role == 'admin'
