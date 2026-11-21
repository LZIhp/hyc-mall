import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'phone_number', 'email', 'password', 'password_confirm')

    def validate_password(self, value):
        if not re.search(r'[a-zA-Z]', value) or not re.search(r'\d', value):
            raise serializers.ValidationError('密码需至少 8 位且包含字母和数字')
        return value

    def validate_phone_number(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('请输入有效的 11 位手机号')
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError('手机号已被注册')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': '两次密码不一致'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs['phone_number']
        password = attrs['password']
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError('手机号或密码错误')
        if not user.check_password(password):
            raise serializers.ValidationError('手机号或密码错误')
        if not user.is_active:
            raise serializers.ValidationError('账号已被禁用')
        refresh = RefreshToken.for_user(user)
        refresh['role'] = 'user'
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': user.id,
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone_number', 'email', 'avatar')
        read_only_fields = ('id',)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    new_password_confirm = serializers.CharField()


class UpdateAvatarSerializer(serializers.Serializer):
    avatar = serializers.CharField()
