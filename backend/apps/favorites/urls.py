from django.urls import path

from . import views

urlpatterns = [
    path('', views.FavoriteListCreateView.as_view(), name='favorite-list-create'),
    path('batch-delete/', views.FavoriteBatchDeleteView.as_view(), name='favorite-batch-delete'),
    path('<int:favorite_id>/', views.FavoriteDetailView.as_view(), name='favorite-detail'),
]
