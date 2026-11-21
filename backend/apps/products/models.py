from django.db import models


class Product(models.Model):
    """商品"""
    product_id = models.BigAutoField(primary_key=True)
    name = models.CharField('商品名称', max_length=200)
    description = models.TextField('描述', null=True, blank=True)
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    category = models.CharField('分类', max_length=50)
    is_active = models.BooleanField('上架', default=True)
    image = models.JSONField('商品图片', null=True, blank=True)
    shop = models.ForeignKey(
        'shops.Shop',
        on_delete=models.CASCADE,
        related_name='products',
        db_constraint=False,
    )
    merchant_name = models.CharField('商家名称', max_length=100, null=True, blank=True)
    shop_name = models.CharField('店铺名称', max_length=100, null=True, blank=True)
    sales = models.IntegerField('销量', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'product'
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
