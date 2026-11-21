from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='user-register'),
    path('login/', views.LoginView.as_view(), name='user-login'),
    path('profile/', views.ProfileView.as_view(), name='user-profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='user-change-password'),
    path('update-avatar/', views.UpdateAvatarView.as_view(), name='user-update-avatar'),
]
