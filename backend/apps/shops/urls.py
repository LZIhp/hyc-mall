from django.urls import path

from apps.products.views import ShopProductsView
from . import views

urlpatterns = [
    path('', views.ShopListCreateView.as_view(), name='shop-list-create'),
    path('<int:shop_id>/', views.ShopDetailView.as_view(), name='shop-detail'),
    path('<int:shop_id>/review/', views.ShopReviewView.as_view(), name='shop-review'),
    path('<int:shop_id>/products/', ShopProductsView.as_view(), name='shop-products'),
]
