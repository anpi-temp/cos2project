from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    USERNAME_FIELD = 'username'

CustomUser = get_user_model()

class AdminMessage(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_admin_messages')
    subject = models.CharField(max_length=255)

    def __str__(self):
        return f"Message to {self.recipient}: {self.subject}"
