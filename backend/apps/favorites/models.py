from django.db import models


class Favorite(models.Model):
    """收藏"""
    favorite_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='favorites',
        db_constraint=False,
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='favorited_by',
        db_constraint=False,
    )
    category = models.CharField('自定义分类', max_length=50, null=True, blank=True)
    note = models.TextField('备注', null=True, blank=True)
    created_at = models.DateTimeField('收藏时间', auto_now_add=True)

    class Meta:
        db_table = 'favorite'
        verbose_name = '收藏'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='uk_fav_user_product'),
        ]

    def __str__(self):
        return f'{self.user_id} -> {self.product_id}'
