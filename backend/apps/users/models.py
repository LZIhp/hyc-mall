from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """用户（顾客）账号；管理员复用本模型（is_staff=True）"""
    phone_number = models.CharField('手机号', max_length=20, unique=True, null=True, blank=True)
    avatar = models.CharField('头像URL', max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username or self.phone_number or str(self.id)
