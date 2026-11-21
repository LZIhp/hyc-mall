from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class Merchant(AbstractBaseUser):
    """商家账号（独立认证模型，手机号登录）"""
    user_id = models.BigAutoField(primary_key=True)
    name = models.CharField('商家名称', max_length=100, unique=True)
    phone_number = models.CharField('联系电话', max_length=20, unique=True)
    email = models.EmailField('邮箱', unique=True, null=True, blank=True)
    password = models.CharField('密码', max_length=128)
    is_active = models.BooleanField('启用', default=True)
    last_login_time = models.DateTimeField('最后登录', null=True, blank=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name', 'email']

    class Meta:
        db_table = 'merchant'
        verbose_name = '商家'
        verbose_name_plural = verbose_name

    @property
    def id(self):
        """兼容 simplejwt 的 for_user，返回主键 user_id"""
        return self.user_id

    def __str__(self):
        return self.name


class Staff(models.Model):
    """商家下属员工"""
    name = models.CharField('姓名', max_length=50)
    phone_number = models.CharField('手机号', max_length=20)
    password = models.CharField('密码', max_length=128)
    shop = models.ForeignKey(
        'shops.Shop',
        on_delete=models.CASCADE,
        related_name='staffs',
        db_constraint=False,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'staff'
        verbose_name = '员工'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
