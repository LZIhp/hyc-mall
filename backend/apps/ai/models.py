from django.db import models


class AIRecommendation(models.Model):
    """AI 推荐记录"""
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='ai_recommendations', db_constraint=False,
    )
    product_ids = models.JSONField('推荐商品ID列表')
    reason = models.TextField('推荐理由', null=True, blank=True)
    created_at = models.DateTimeField('生成时间', auto_now_add=True)

    class Meta:
        db_table = 'ai_recommendation'
        verbose_name = 'AI推荐记录'
        verbose_name_plural = verbose_name


class AICopywriting(models.Model):
    """AI 商品文案"""
    merchant = models.ForeignKey(
        'merchants.Merchant', on_delete=models.CASCADE, related_name='ai_copywritings', db_constraint=False,
    )
    product = models.ForeignKey(
        'products.Product', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='ai_copywritings', db_constraint=False,
    )
    title = models.CharField('标题', max_length=200, null=True, blank=True)
    description = models.TextField('描述', null=True, blank=True)
    selling_points = models.JSONField('卖点列表', null=True, blank=True)
    created_at = models.DateTimeField('生成时间', auto_now_add=True)

    class Meta:
        db_table = 'ai_copywriting'
        verbose_name = 'AI文案'
        verbose_name_plural = verbose_name


class AIAssistantSession(models.Model):
    """购物助手会话"""
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='ai_sessions', db_constraint=False,
    )
    title = models.CharField('会话标题', max_length=200, null=True, blank=True)
    messages = models.JSONField('对话消息', default=list)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'ai_assistant_session'
        verbose_name = '助手会话'
        verbose_name_plural = verbose_name
