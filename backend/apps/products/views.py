from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from common.permissions import IsMerchant
from .models import Product
from .serializers import ProductSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    """商品列表/搜索（公开）+ 添加商品（商家）"""
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsMerchant()]
        return []

    def get_queryset(self):
        qs = super().get_queryset().filter(is_active=True)
        category = self.request.query_params.get('category')
        keyword = self.request.query_params.get('keyword')
        shop_id = self.request.query_params.get('shop_id')
        if category:
            qs = qs.filter(category=category)
        if keyword:
            qs = qs.filter(name__icontains=keyword)
        if shop_id:
            qs = qs.filter(shop_id=shop_id)
        return qs

    def perform_create(self, serializer):
        shop = serializer.validated_data.get('shop')
        serializer.save(
            shop_name=shop.name,
            merchant_name=shop.merchant_name,
        )


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """商品详情（公开）+ 编辑/删除（商家本人）"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'product_id'

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return [IsMerchant()]
        return []

    def get_object(self):
        obj = super().get_object()
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            if obj.shop.merchant_id != self.request.user.user_id:
                raise PermissionDenied('无权操作该商品')
        return obj


class ShopProductsView(generics.ListAPIView):
    """店铺商品列表（公开）"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return Product.objects.filter(shop_id=shop_id, is_active=True).order_by('-created_at')
