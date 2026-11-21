from django.db import models


class Shop(models.Model):
    """店铺"""
    shop_id = models.BigAutoField(primary_key=True)
    name = models.CharField('店铺名称', max_length=100)
    address = models.CharField('店铺地址', max_length=255)
    phone_number = models.CharField('联系电话', max_length=20)
    description = models.TextField('简介', null=True, blank=True)
    latitude = models.DecimalField('纬度', max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField('经度', max_digits=10, decimal_places=6, null=True, blank=True)
    photo = models.ImageField('营业执照/头像', upload_to='shops/', null=True, blank=True)
    shop_photos = models.JSONField('店铺照片', null=True, blank=True)
    status = models.CharField('审核状态', max_length=20, default='pending')
    merchant = models.ForeignKey(
        'merchants.Merchant',
        on_delete=models.CASCADE,
        related_name='shops',
        db_constraint=False,
    )
    merchant_name = models.CharField('商家名称', max_length=100, null=True, blank=True)
    merchant_phone = models.CharField('商家电话', max_length=20, null=True, blank=True)
    open_time = models.CharField('开店时间', max_length=50, null=True, blank=True)
    service_phone = models.CharField('客服电话', max_length=20, null=True, blank=True)
    business_hours = models.CharField('营业时间', max_length=100, null=True, blank=True)
    rating = models.DecimalField('评分', max_digits=2, decimal_places=1, default=4.7)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'shop'
        verbose_name = '店铺'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
