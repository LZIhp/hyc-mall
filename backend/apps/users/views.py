from rest_framework import generics
from rest_framework.response import Response

from common.permissions import IsUser
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    UpdateAvatarSerializer,
)


class RegisterView(generics.CreateAPIView):
    """用户注册"""
    serializer_class = UserRegisterSerializer


class LoginView(generics.GenericAPIView):
    """用户登录"""
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class ProfileView(generics.RetrieveUpdateAPIView):
    """获取/更新个人信息"""
    permission_classes = [IsUser]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.GenericAPIView):
    """修改密码"""
    permission_classes = [IsUser]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')
        if not request.user.check_password(old_password):
            return Response({'old_password': '旧密码错误'}, status=400)
        if new_password != new_password_confirm:
            return Response({'new_password_confirm': '两次密码不一致'}, status=400)
        if len(new_password) < 8:
            return Response({'new_password': '密码至少 8 位'}, status=400)
        request.user.set_password(new_password)
        request.user.save()
        return Response({'message': '密码修改成功'})


class UpdateAvatarView(generics.GenericAPIView):
    """更新头像"""
    permission_classes = [IsUser]
    serializer_class = UpdateAvatarSerializer

    def post(self, request):
        avatar = request.data.get('avatar')
        if not avatar:
            return Response({'avatar': '头像不能为空'}, status=400)
        request.user.avatar = avatar
        request.user.save()
        return Response({'avatar': avatar})
