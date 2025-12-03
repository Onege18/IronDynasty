from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import ClientProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_client_profile(sender, instance, created, **kwargs):
    """
    Автоматическое создание профиля только для пользователей с ролью 'client'
    """
    if created and instance.role == "client":
        ClientProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_client_profile(sender, instance, **kwargs):
    """
    Безопасное сохранение профиля.
    Если роль изменилась позже — создаем профиль при необходимости.
    """
    if instance.role == "client":
        ClientProfile.objects.get_or_create(user=instance)
        instance.client_profile.save()
