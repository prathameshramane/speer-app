from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='get_access_token'),
    path('signup', RegisterView.as_view(), name='register_user'),
    path('refresh', TokenRefreshView.as_view(), name='refresh_access_token'),
]