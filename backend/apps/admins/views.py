from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response

from common.permissions import IsAdmin
from apps.merchants.models import Merchant
from apps.shops.models import Shop
from apps.products.models import Product
from .serializers import (
    AdminLoginSerializer,
    AdminUserSerializer,
    AdminMerchantSerializer,
    PendingShopSerializer,
    AdminProductSerializer,
    DashboardSerializer,
)

User = get_user_model()


class AdminLoginView(generics.GenericAPIView):
    """管理员登录"""
    serializer_class = AdminLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class PendingShopListView(generics.ListAPIView):
    """待审核店铺列表"""
    permission_classes = [IsAdmin]
    serializer_class = PendingShopSerializer

    def list(self, request, *args, **kwargs):
        shops = Shop.objects.filter(status='pending').order_by('-created_at')
        return Response({'pending_shops': PendingShopSerializer(shops, many=True).data})


class AdminShopListView(generics.ListAPIView):
    """管理员店铺列表（全部）"""
    permission_classes = [IsAdmin]
    serializer_class = PendingShopSerializer
    queryset = Shop.objects.all().order_by('-created_at')


class AdminProductListView(generics.ListAPIView):
    """管理员商品列表（全部）"""
    permission_classes = [IsAdmin]
    serializer_class = AdminProductSerializer
    queryset = Product.objects.all().order_by('-created_at')


class AdminProductDeleteView(generics.DestroyAPIView):
    """管理员删除商品"""
    permission_classes = [IsAdmin]
    serializer_class = AdminProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'product_id'


class AdminUserListView(generics.ListAPIView):
    """用户列表"""
    permission_classes = [IsAdmin]
    serializer_class = AdminUserSerializer
    queryset = User.objects.all().order_by('-date_joined')


class AdminUserUpdateView(generics.UpdateAPIView):
    """禁用/启用用户"""
    permission_classes = [IsAdmin]
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        is_active = request.data.get('is_active')
        if is_active is None:
            return Response({'is_active': 'is_active 不能为空'}, status=400)
        user.is_active = is_active
        user.save()
        return Response(AdminUserSerializer(user).data)


class AdminMerchantListView(generics.ListAPIView):
    """商家列表"""
    permission_classes = [IsAdmin]
    serializer_class = AdminMerchantSerializer
    queryset = Merchant.objects.all().order_by('-user_id')


class AdminMerchantUpdateView(generics.UpdateAPIView):
    """禁用/启用商家"""
    permission_classes = [IsAdmin]
    serializer_class = AdminMerchantSerializer
    queryset = Merchant.objects.all()
    lookup_field = 'user_id'

    def patch(self, request, *args, **kwargs):
        merchant = self.get_object()
        is_active = request.data.get('is_active')
        if is_active is None:
            return Response({'is_active': 'is_active 不能为空'}, status=400)
        merchant.is_active = is_active
        merchant.save()
        return Response(AdminMerchantSerializer(merchant).data)


class DashboardView(generics.GenericAPIView):
    """数据看板"""
    permission_classes = [IsAdmin]
    serializer_class = DashboardSerializer

    def get(self, request):
        return Response({
            'shop_count': Shop.objects.count(),
            'pending_shop_count': Shop.objects.filter(status='pending').count(),
            'product_count': Product.objects.count(),
            'user_count': User.objects.count(),
            'merchant_count': Merchant.objects.count(),
        })
