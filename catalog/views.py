from django.db.models import Q
from django.views.generic import DetailView, ListView

from .models import Category, Product


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        queryset = (
            Product.objects.select_related("category")
            .filter(active=True)
        )

        search_query = self.request.GET.get("q", "").strip()
        condition = self.request.GET.get("condition", "").strip()
        category_slug = self.request.GET.get("category", "").strip()
        sort = self.request.GET.get("sort", "featured").strip()

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(category__name__icontains=search_query)
            )

        valid_conditions = {
            value
            for value, label in Product.Condition.choices
        }

        if condition in valid_conditions:
            queryset = queryset.filter(
                condition=condition
            )

        if category_slug:
            queryset = queryset.filter(
                category__slug=category_slug,
                category__active=True,
            )

        if sort == "price_low":
            queryset = queryset.order_by(
                "sgng_price",
                "name",
            )

        elif sort == "price_high":
            queryset = queryset.order_by(
                "-sgng_price",
                "name",
            )

        elif sort == "newest":
            queryset = queryset.order_by(
                "-created_at",
            )

        elif sort == "name":
            queryset = queryset.order_by(
                "name",
            )

        else:
            queryset = queryset.order_by(
                "-featured",
                "-created_at",
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = (
            Category.objects.filter(active=True)
            .order_by("name")
        )

        context["condition_choices"] = (
            Product.Condition.choices
        )

        context["current_search"] = (
            self.request.GET.get("q", "").strip()
        )

        context["current_condition"] = (
            self.request.GET.get(
                "condition",
                "",
            ).strip()
        )

        context["current_category"] = (
            self.request.GET.get(
                "category",
                "",
            ).strip()
        )

        context["current_sort"] = (
            self.request.GET.get(
                "sort",
                "featured",
            ).strip()
        )

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return (
            Product.objects.select_related("category")
            .filter(active=True)
        )
