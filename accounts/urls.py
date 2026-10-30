from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import SGnGLoginView, SignUpView


app_name = "accounts"


urlpatterns = [
    path(
        "register/",
        SignUpView.as_view(),
        name="register",
    ),

    path(
        "login/",
        SGnGLoginView.as_view(),
        name="login",
    ),

    path(
        "logout/",
        LogoutView.as_view(
            next_page="pages:home"
        ),
        name="logout",
    ),
]