from django.urls import path
from .views import CustomUserCreate, BlacklistTokenUpdateView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'users'

urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('login/', CustomTokenObtainPairView.as_view(), name="auth_user"),
    path('logout/', BlacklistTokenUpdateView.as_view(), name="deauth_user"),
    path('refresh/', TokenRefreshView.as_view(), name="token_refresh"),
]
