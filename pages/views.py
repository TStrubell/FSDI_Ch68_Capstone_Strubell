from django.views.generic import TemplateView
from django.shortcuts import render

from catalog.models import Product


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["featured_products"] = (
            Product.objects
            .select_related("category")
            .filter(
                active=True,
                featured=True,
            )
            .order_by("-created_at")[:3]
        )

        return context

class MilitaryServiceView(TemplateView):
    template_name = "about/military_service.html"


class CraftsmanshipView(TemplateView):
    template_name = "about/craftsmanship.html"


class EntrepreneurshipView(TemplateView):
    template_name = "about/entrepreneurship.html"


class SoftwareDevelopmentView(TemplateView):
    template_name = "about/software_development.html"


class AboutView(TemplateView):
    template_name = "pages/about.html"


def terms_of_service(request):
    return render(request, "pages/terms_of_service.html")


def privacy_policy(request):
    return render(request, "pages/privacy_policy.html")
