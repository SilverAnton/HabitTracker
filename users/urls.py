from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework.permissions import AllowAny

from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter
from users.views import UsersViewSet, UserCreateApiView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r"users", UsersViewSet)


app_name = UsersConfig.name

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserCreateApiView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]
