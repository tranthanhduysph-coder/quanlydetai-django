from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # API cho Auth
    path('register/', views.register_user, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API cho nghiệp vụ
    path('de-cuong/', views.de_cuong_view, name='de-cuong-api'),
    path('goi-y-ai/', views.goi_y_ai, name='goi-y-ai-api'),
    
    # API cho download (Giữ nguyên /pdf/ nhưng trỏ đến hàm tạo Word)
    path('de-cuong/pdf/', views.download_pdf_view, name='de-cuong-pdf'),
]