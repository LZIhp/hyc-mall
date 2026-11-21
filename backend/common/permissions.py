from rest_framework.permissions import BasePermission


def get_role(request):
    """从 JWT payload 读取角色声明（user / merchant / admin）"""
    auth = getattr(request, 'auth', None)
    if auth is not None and hasattr(auth, 'payload'):
        return auth.payload.get('role')
    return None


class IsUser(BasePermission):
    """仅「用户」角色可访问"""

    def has_permission(self, request, view):
        return bool(
            request.user
            and getattr(request.user, 'is_authenticated', False)
            and get_role(request) == 'user'
        )


class IsMerchant(BasePermission):
    """仅「商家」角色可访问"""

    def has_permission(self, request, view):
        return bool(
            request.user
            and getattr(request.user, 'is_authenticated', False)
            and get_role(request) == 'merchant'
        )


class IsAdmin(BasePermission):
    """仅「管理员」角色可访问"""

    def has_permission(self, request, view):
        return bool(
            request.user
            and getattr(request.user, 'is_authenticated', False)
            and get_role(request) == 'admin'
        )
