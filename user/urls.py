from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import LoginInitial, LoginComplete


urlpatterns = [
    path("login/initial/", LoginInitial.as_view(), name="login-initial"),
    path("login/complete/", LoginComplete.as_view(), name="login-complete"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
