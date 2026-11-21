import re

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Merchant, Staff


class MerchantRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = Merchant
        fields = ('user_id', 'name', 'phone_number', 'email', 'password', 'password_confirm')

    def validate_password(self, value):
        if not re.search(r'[a-zA-Z]', value) or not re.search(r'\d', value):
            raise serializers.ValidationError('密码需至少 8 位且包含字母和数字')
        return value

    def validate_phone_number(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('请输入有效的 11 位手机号')
        if Merchant.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError('手机号已被注册')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': '两次密码不一致'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        merchant = Merchant(**validated_data)
        merchant.set_password(password)
        merchant.save()
        return merchant


class MerchantLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            merchant = Merchant.objects.get(phone_number=attrs['phone_number'])
        except Merchant.DoesNotExist:
            raise serializers.ValidationError('手机号或密码错误')
        if not merchant.check_password(attrs['password']):
            raise serializers.ValidationError('手机号或密码错误')
        if not merchant.is_active:
            raise serializers.ValidationError('账号已被禁用')
        refresh = RefreshToken.for_user(merchant)
        refresh['role'] = 'merchant'
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'merchant': {'user_id': merchant.user_id},
        }


class StaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = Staff
        fields = ('id', 'name', 'phone_number', 'password', 'password_confirm', 'shop')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': '两次密码不一致'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        staff = Staff(**validated_data)
        staff.set_password(password)
        staff.save()
        return staff


class MerchantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ('user_id', 'name', 'phone_number', 'email', 'is_active', 'last_login_time')
        read_only_fields = ('user_id', 'is_active', 'last_login_time')
