from django.urls import path
from .views import UserViewSet, BlacklistTokenUpdateView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers
app_name = 'users'

router = routers.SimpleRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    *router.urls,
    path('login/', CustomTokenObtainPairView.as_view(), name="auth_user"),
    path('logout/', BlacklistTokenUpdateView.as_view(), name="deauth_user"),
    path('refresh/', TokenRefreshView.as_view(), name="token_refresh"),
]

