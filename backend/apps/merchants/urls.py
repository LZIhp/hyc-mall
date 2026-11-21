from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.MerchantRegisterView.as_view(), name='merchant-register'),
    path('login/', views.MerchantLoginView.as_view(), name='merchant-login'),
    path('profile/', views.MerchantProfileView.as_view(), name='merchant-profile'),
    path('staffs/', views.StaffCreateView.as_view(), name='staff-create'),
]
