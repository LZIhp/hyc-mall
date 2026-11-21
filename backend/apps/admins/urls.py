from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.AdminLoginView.as_view(), name='admin-login'),
    path('pending-shops/', views.PendingShopListView.as_view(), name='admin-pending-shops'),
    path('shops/', views.AdminShopListView.as_view(), name='admin-shops'),
    path('products/', views.AdminProductListView.as_view(), name='admin-products'),
    path('products/<int:product_id>/', views.AdminProductDeleteView.as_view(), name='admin-product-delete'),
    path('users/', views.AdminUserListView.as_view(), name='admin-users'),
    path('users/<int:pk>/', views.AdminUserUpdateView.as_view(), name='admin-user-update'),
    path('merchants/', views.AdminMerchantListView.as_view(), name='admin-merchants'),
    path('merchants/<int:user_id>/', views.AdminMerchantUpdateView.as_view(), name='admin-merchant-update'),
    path('dashboard/', views.DashboardView.as_view(), name='admin-dashboard'),
]
