from rest_framework import serializers

from .models import Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'
        read_only_fields = (
            'shop_id', 'merchant', 'merchant_name', 'merchant_phone',
            'created_at', 'updated_at',
        )


class ShopReviewSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['approved', 'rejected', 'suspended'])
