from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from common.permissions import IsUser
from apps.products.models import Product
from .models import Favorite
from .serializers import FavoriteSerializer, FavoriteBatchDeleteSerializer


class FavoriteListCreateView(generics.ListCreateAPIView):
    """收藏列表（用户）+ 添加收藏"""
    permission_classes = [IsUser]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        qs = Favorite.objects.filter(user=self.request.user)
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs.order_by('-created_at')

    def perform_create(self, serializer):
        product_id = self.request.data.get('product')
        if not product_id:
            raise ValidationError({'product': '商品不能为空'})
        product = Product.objects.filter(product_id=product_id).first()
        if not product:
            raise ValidationError({'product': '商品不存在'})
        if Favorite.objects.filter(user=self.request.user, product=product).exists():
            raise ValidationError({'product': '已收藏该商品'})
        serializer.save(user=self.request.user, product=product)


class FavoriteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """更新收藏（分类/备注）+ 取消收藏"""
    permission_classes = [IsUser]
    serializer_class = FavoriteSerializer
    lookup_field = 'favorite_id'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class FavoriteBatchDeleteView(generics.GenericAPIView):
    """批量删除收藏"""
    permission_classes = [IsUser]
    serializer_class = FavoriteBatchDeleteSerializer

    def post(self, request):
        ids = request.data.get('ids', [])
        if not ids:
            return Response({'ids': 'ids 不能为空'}, status=400)
        Favorite.objects.filter(user=request.user, favorite_id__in=ids).delete()
        return Response({'deleted': True})
