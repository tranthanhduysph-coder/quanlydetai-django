# core/urls.py
from django.urls import path
from . import views
# Thêm dòng này để lấy API Đăng nhập/Token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('de-cuong/', views.de_cuong_view, name='de-cuong-api'),
    path('goi-y-ai/', views.goi_y_ai, name='goi-y-ai-api'),
    # API để lấy Token (Đăng nhập)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]