from rest_framework_simplejwt.authentication import JWTAuthentication


class RoleBasedJWTAuthentication(JWTAuthentication):
    """根据 token 的 role 声明，用对应模型解析用户。

    - role=merchant → Merchant 模型
    - role=user / admin → 自定义 User 模型
    """

    def get_user(self, validated_token):
        role = validated_token.get('role')
        if role == 'merchant':
            from apps.merchants.models import Merchant
            user_id = validated_token.get('user_id')
            try:
                return Merchant.objects.get(user_id=user_id)
            except Merchant.DoesNotExist:
                return None
        return super().get_user(validated_token)


from drf_spectacular.extensions import OpenApiAuthenticationExtension


class RoleBasedJWTAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = 'common.auth.RoleBasedJWTAuthentication'
    name = 'jwtAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }
