from django.contrib import admin
from django.urls import path, include
from .viewsets import UserView, RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/api/', include('rest_framework.urls'), name='auth_login'),
    path('auth/user/', UserView.as_view(), name='user_detail'),
    path('auth/admin/', admin.site.urls, name='admin'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='register'),
]
