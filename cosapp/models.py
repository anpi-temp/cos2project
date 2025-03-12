from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    is_admin_user = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

class AdminMessage(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_admin_messages')
    subject = models.CharField(max_length=255)

    def __str__(self):
        return f"Message to {self.recipient}: {self.subject}"

class AdminManager(BaseUserManager):
    def create_admin(self, username, password=None):
        if not username:
            raise ValueError('Admins must have a username')
        admin = self.model(username=username, is_staff=True, is_superuser=True)
        admin.set_password(password)
        admin.save(using=self._db)
        return admin

class CustomAdmin(CustomUser):
    is_first_login = models.BooleanField(default=True)

    objects = AdminManager()

    def save(self, *args, **kwargs):
        self.is_admin_user = True
        self.is_staff = True  # Django管理画面にアクセスできるようにする
        self.is_superuser = True  # すべての権限を付与する
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
