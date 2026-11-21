from rest_framework import serializers

from apps.shops.models import Shop
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    shop_id = serializers.PrimaryKeyRelatedField(source='shop', queryset=Shop.objects.all())

    class Meta:
        model = Product
        fields = (
            'product_id', 'name', 'description', 'price', 'category', 'is_active',
            'image', 'shop_id', 'merchant_name', 'shop_name', 'sales',
            'created_at', 'updated_at',
        )
        read_only_fields = (
            'product_id', 'merchant_name', 'shop_name', 'sales',
            'created_at', 'updated_at',
        )
