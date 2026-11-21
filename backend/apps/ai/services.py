"""AI 能力调用层。

当前为 mock 占位实现，后续接入真实 LLM（Claude API）时，仅需替换本模块内的函数实现。
"""


def generate_recommendations(user, limit=10):
    """生成个性化商品推荐（mock：返回最新商品）"""
    from apps.products.models import Product
    products = list(Product.objects.filter(is_active=True)[:limit])
    return [
        {'product_id': p.product_id, 'reason': '根据你的浏览与收藏偏好为你推荐'}
        for p in products
    ]


def generate_copywriting(name, category, selling_points):
    """生成商品文案（mock）"""
    points = selling_points if isinstance(selling_points, list) else [selling_points]
    points_text = '、'.join(points)
    return {
        'title': name,
        'description': f'{name}，精选{category}品类，{points_text}，值得信赖。',
        'selling_points': points,
    }


def assistant_reply(message):
    """购物助手回复（mock）"""
    from apps.products.models import Product
    products = list(Product.objects.filter(is_active=True)[:3])
    return {
        'reply': f'根据你的需求「{message}」，为你推荐以下商品',
        'products': [{'product_id': p.product_id, 'name': p.name, 'price': str(p.price)} for p in products],
        'suggestions': ['关注商品口碑与评价', '结合预算筛选', '优先选择评分高的店铺'],
    }
