from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.merchants.models import Merchant
from apps.shops.models import Shop
from apps.products.models import Product

User = get_user_model()


class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(username=attrs['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError('用户名或密码错误')
        if not user.check_password(attrs['password']):
            raise serializers.ValidationError('用户名或密码错误')
        if not user.is_staff:
            raise serializers.ValidationError('非管理员账号')
        refresh = RefreshToken.for_user(user)
        refresh['role'] = 'admin'
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone_number', 'email', 'is_active', 'date_joined')


class AdminMerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ('user_id', 'name', 'phone_number', 'email', 'is_active', 'last_login_time')


class PendingShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('shop_id', 'name', 'address', 'phone_number', 'merchant_name', 'merchant_phone', 'created_at')


class AdminProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_id', 'name', 'category', 'merchant_name', 'shop_name', 'price', 'image', 'created_at', 'updated_at')


class DashboardSerializer(serializers.Serializer):
    shop_count = serializers.IntegerField()
    pending_shop_count = serializers.IntegerField()
    product_count = serializers.IntegerField()
    user_count = serializers.IntegerField()
    merchant_count = serializers.IntegerField()
