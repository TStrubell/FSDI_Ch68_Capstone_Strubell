from django.urls import path

from . import views

from .views import (
    AboutView, 
    HomeView, 
    MilitaryServiceView, 
    CraftsmanshipView, 
    EntrepreneurshipView, 
    SoftwareDevelopmentView,
)


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

    path(
        "about/military-service/",
        MilitaryServiceView.as_view(),
        name="military_service",
    ),

    path(
        "about/craftsmanship/",
        CraftsmanshipView.as_view(),
        name="craftsmanship",
    ),

    path(
        "about/entrepreneurship/",
        EntrepreneurshipView.as_view(),
        name="entrepreneurship",
    ),

    path(
        "about/software-development/",
        SoftwareDevelopmentView.as_view(),
        name="software_development",
    ),
]
