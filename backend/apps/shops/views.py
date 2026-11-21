from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from common.permissions import IsMerchant, IsAdmin
from .models import Shop
from .serializers import ShopSerializer, ShopReviewSerializer


class ShopListCreateView(generics.ListCreateAPIView):
    """店铺列表（公开）+ 创建店铺（商家）"""
    queryset = Shop.objects.all().order_by('-created_at')
    serializer_class = ShopSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsMerchant()]
        return []

    def perform_create(self, serializer):
        merchant = self.request.user
        serializer.save(
            merchant=merchant,
            merchant_name=merchant.name,
            merchant_phone=merchant.phone_number,
        )


class ShopDetailView(generics.RetrieveUpdateAPIView):
    """店铺详情（公开）+ 编辑店铺（商家本人）"""
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    lookup_field = 'shop_id'

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            return [IsMerchant()]
        return []

    def get_object(self):
        obj = super().get_object()
        if self.request.method in ('PUT', 'PATCH'):
            if obj.merchant_id != self.request.user.user_id:
                raise PermissionDenied('无权操作该店铺')
        return obj


class ShopReviewView(generics.GenericAPIView):
    """店铺审核（管理员）"""
    permission_classes = [IsAdmin]
    serializer_class = ShopReviewSerializer

    def patch(self, request, shop_id):
        shop = Shop.objects.filter(shop_id=shop_id).first()
        if not shop:
            return Response({'detail': '店铺不存在'}, status=404)
        status_val = request.data.get('status')
        if status_val not in ('approved', 'rejected', 'suspended'):
            return Response({'status': '无效的状态'}, status=400)
        shop.status = status_val
        shop.save()
        return Response(ShopSerializer(shop).data)
