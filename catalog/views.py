from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.messages.views import SuccessMessageMixin

from django.db.models import Q

from django.urls import reverse_lazy

from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ProductForm

from .models import Category, Product


# =========================================================
# PUBLIC MARKETPLACE
# =========================================================


class ProductListView(ListView):
    """
    Public SGnG Marketplace catalog.
    """

    model = Product

    template_name = (
        "catalog/product_list.html"
    )

    context_object_name = "products"

    paginate_by = 12

    def get_queryset(self):
        queryset = (
            Product.objects
            .select_related("category")
            .filter(
                active=True,
                category__active=True,
            )
        )

        search_query = (
            self.request.GET
            .get("q", "")
            .strip()
        )

        condition = (
            self.request.GET
            .get("condition", "")
            .strip()
        )

        category_slug = (
            self.request.GET
            .get("category", "")
            .strip()
        )

        sort = (
            self.request.GET
            .get(
                "sort",
                "featured",
            )
            .strip()
        )

        if search_query:
            queryset = queryset.filter(
                Q(
                    name__icontains=
                    search_query
                )
                |
                Q(
                    description__icontains=
                    search_query
                )
                |
                Q(
                    category__name__icontains=
                    search_query
                )
            )

        valid_conditions = {
            value
            for value, label
            in Product.Condition.choices
        }

        if condition in valid_conditions:
            queryset = queryset.filter(
                condition=condition
            )

        if category_slug:
            queryset = queryset.filter(
                category__slug=
                category_slug
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
                "-created_at"
            )

        elif sort == "name":
            queryset = queryset.order_by(
                "name"
            )

        else:
            queryset = queryset.order_by(
                "-featured",
                "-created_at",
            )

        return queryset

    def get_context_data(
        self,
        **kwargs,
    ):
        context = (
            super()
            .get_context_data(
                **kwargs
            )
        )

        context["categories"] = (
            Category.objects
            .filter(active=True)
            .order_by("name")
        )

        context[
            "condition_choices"
        ] = Product.Condition.choices

        context["current_search"] = (
            self.request.GET
            .get("q", "")
            .strip()
        )

        context[
            "current_condition"
        ] = (
            self.request.GET
            .get(
                "condition",
                "",
            )
            .strip()
        )

        context[
            "current_category"
        ] = (
            self.request.GET
            .get(
                "category",
                "",
            )
            .strip()
        )

        context["current_sort"] = (
            self.request.GET
            .get(
                "sort",
                "featured",
            )
            .strip()
        )

        return context


class ProductDetailView(DetailView):
    """
    Public Product Detail page.
    """

    model = Product

    template_name = (
        "catalog/"
        "product_detail.html"
    )

    context_object_name = "product"

    def get_queryset(self):
        return (
            Product.objects
            .select_related("category")
            .filter(
                active=True,
                category__active=True,
            )
        )


# =========================================================
# STAFF SECURITY MIXIN
# =========================================================


class StaffRequiredMixin(
    LoginRequiredMixin,
    UserPassesTestMixin,
):
    """
    Restrict a view to authenticated Django staff users.
    """

    login_url = reverse_lazy(
        "accounts:login"
    )

    permission_denied_message = (
        "Staff access is required "
        "to manage marketplace products."
    )

    def test_func(self):
        user = self.request.user

        return (
            user.is_authenticated
            and user.is_staff
        )


# =========================================================
# STAFF PRODUCT MANAGEMENT
# =========================================================


class ProductManagementView(
    StaffRequiredMixin,
    ListView,
):
    """
    Staff-facing Product Management page.
    """

    model = Product

    template_name = (
        "catalog/product_management.html"
    )

    context_object_name = "products"

    paginate_by = 20

    def get_queryset(self):
        return (
            Product.objects
            .select_related("category")
            .order_by(
                "-featured",
                "name",
            )
        )

    def get_context_data(
        self,
        **kwargs,
    ):
        context = super().get_context_data(
            **kwargs
        )

        all_products = Product.objects.all()

        context["active_count"] = (
            all_products
            .filter(active=True)
            .count()
        )

        context["featured_count"] = (
            all_products
            .filter(featured=True)
            .count()
        )

        context["out_of_stock_count"] = (
            all_products
            .filter(
                inventory_quantity=0
            )
            .count()
        )

        context["category_count"] = (
            Category.objects.count()
        )

        return context


class ProductCreateView(
    StaffRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    """
    Create a new marketplace product.
    """

    model = Product

    form_class = ProductForm

    template_name = (
        "catalog/product_form.html"
    )

    success_message = (
        "Product created successfully."
    )

    def form_valid(
        self,
        form,
    ):
        messages.success(
            self.request,
            (
                "Product created "
                "successfully."
            ),
        )

        return super().form_valid(
            form
        )


class ProductUpdateView(
    StaffRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    """
    Update an existing marketplace product.
    """

    model = Product

    form_class = ProductForm

    template_name = (
        "catalog/product_form.html"
    )

    success_message = (
        "Product updated successfully."
    )

    context_object_name = (
        "product"
    )

    def get_queryset(self):
        return (
            Product.objects
            .select_related("category")
        )

    def form_valid(
        self,
        form,
    ):
        messages.success(
            self.request,
            (
                "Product updated "
                "successfully."
            ),
        )

        return super().form_valid(
            form
        )


class ProductDeleteView(
    StaffRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    """
    Delete a marketplace product after confirmation.
    """

    model = Product

    template_name = (
        "catalog/product_confirm_delete.html"
    )

    context_object_name = (
        "product"
    )

    success_url = reverse_lazy(
        "catalog:product-management"
    )

    success_message = (
        "Product deleted successfully."
    )

    def form_valid(
        self,
        form,
    ):
        product_name = (
            self.object.name
        )

        messages.success(
            self.request,
            (
                f"{product_name} "
                "was deleted successfully."
            ),
        )

        return super().form_valid(
            form
        )