from django.urls import path

from . import views

from .views import AboutView, HomeView


app_name = "pages"


urlpatterns = [
    path(
        "",
        HomeView.as_view(),
        name="home",
    ),

    path(
        "about/",
        AboutView.as_view(),
        name="about",
    ),

    path(
        "terms-of-service/",
        views.terms_of_service,
        name="terms_of_service",
    ),
    path(
        "privacy-policy/",
        views.privacy_policy,
        name="privacy_policy",
    ),
]
