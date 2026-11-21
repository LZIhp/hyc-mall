from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # 业务路由
    path('api/users/favorites/', include('apps.favorites.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/merchants/', include('apps.merchants.urls')),
    path('api/admins/', include('apps.admins.urls')),
    path('api/shops/', include('apps.shops.urls')),
    path('api/products/', include('apps.products.urls')),
    path('api/ai/', include('apps.ai.urls')),
]
