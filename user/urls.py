from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import ManageUserView, CreateUserView

app_name = 'user'

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('me/', ManageUserView.as_view(), name='manage-user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
