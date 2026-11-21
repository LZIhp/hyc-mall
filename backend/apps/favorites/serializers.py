from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    product_detail = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ('favorite_id', 'user', 'product', 'category', 'note', 'created_at', 'product_detail')
        read_only_fields = ('favorite_id', 'user', 'created_at')

    @extend_schema_field(serializers.DictField())
    def get_product_detail(self, obj):
        p = obj.product
        if not p:
            return None
        return {
            'product_id': p.product_id,
            'name': p.name,
            'price': str(p.price),
            'category': p.category,
            'image': p.image,
            'shop_id': p.shop_id,
        }


class FavoriteBatchDeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField())
