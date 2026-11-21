from rest_framework import generics
from rest_framework.response import Response

from common.permissions import IsMerchant
from .serializers import (
    MerchantRegisterSerializer,
    MerchantLoginSerializer,
    StaffSerializer,
    MerchantProfileSerializer,
)


class MerchantRegisterView(generics.CreateAPIView):
    """商家注册"""
    serializer_class = MerchantRegisterSerializer


class MerchantLoginView(generics.GenericAPIView):
    """商家登录"""
    serializer_class = MerchantLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class StaffCreateView(generics.CreateAPIView):
    """添加员工"""
    serializer_class = StaffSerializer


class MerchantProfileView(generics.RetrieveUpdateAPIView):
    """获取/更新商家资料"""
    permission_classes = [IsMerchant]
    serializer_class = MerchantProfileSerializer

    def get_object(self):
        return self.request.user
