from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone
from rest_framework import serializers
from django.utils import timezone

class CustomUser(AbstractUser):
    """
    カスタムユーザーモデル
    """
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="電話番号は '+999999999' の形式で、最大15桁まで入力してください。"
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,  # フォームや管理画面で空の値を許可
        default="",  # デフォルト値として空文字列を設定
        verbose_name="電話番号"
    )
    is_admin = models.BooleanField(default=False, verbose_name="管理者権限")

    class Meta:
        verbose_name = "ユーザー"
        verbose_name_plural = "ユーザー一覧"

    def __str__(self):
        return self.username

    @classmethod
    def create_admin(cls, username, password, phone_number=None):
        """
        管理者ユーザーを作成するためのクラスメソッド
        """
        user = cls.objects.create_user(username=username, password=password, phone_number=phone_number)
        user.is_admin = True
        user.is_staff = True  # 管理画面へのアクセス権を付与
        user.save()
        return user
    
class AdminMessageManager(models.Manager):
    def unread(self):
        return self.filter(is_read=False)

    def read(self):
        return self.filter(is_read=True)


class AdminMessage(models.Model):
    """
    管理者メッセージモデル
    """
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_admin_messages', verbose_name="受信者")
    subject = models.CharField(max_length=255, verbose_name="件名")
    content = models.TextField(verbose_name="本文", default="")  # デフォルト値を設定
    created_at = models.DateTimeField(default=timezone.now, verbose_name="送信日時")
    is_read = models.BooleanField(default=False, verbose_name="既読状態")

    objects = AdminMessageManager()

    class Meta:
        verbose_name = "管理者メッセージ"
        verbose_name_plural = "管理者メッセージ一覧"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} (To: {self.recipient.username})"
    