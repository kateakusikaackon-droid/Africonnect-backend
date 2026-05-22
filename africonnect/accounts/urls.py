from django.urls import path

from .views import (
    UserRegisterView,
    LoginView,
    LogoutView,
    SupplierDashboardView,
    BuyerDashboardView,
    HealthCheckView,
)

from profiles.views import (
    SupplierProfileView,
)

from products.views import (
    ProductCategoryListView,
    ProductListCreateView,
    ProductDetailView,
)

urlpatterns = [

    # =====================================
    # REGISTRATION
    # =====================================

    path(
        "suppliers/register/",
        UserRegisterView.as_view(),
        {"role": "supplier"},
        name="supplier-register"
    ),

    path(
        "buyers/register/",
        UserRegisterView.as_view(),
        {"role": "buyer"},
        name="buyer-register"
    ),

    # =====================================
    # AUTHENTICATION
    # =====================================

    path(
        "login/",
        LoginView.as_view(),
        name="login"
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout"
    ),

    # =====================================
    # SUPPLIER DASHBOARD
    # =====================================

    # DASHBOARD HOME
    path(
        "suppliers/dashboard/",
        SupplierDashboardView.as_view(),
        name="supplier-dashboard"
    ),

    # SUPPLIER PROFILE
    path(
        "suppliers/dashboard/profile/",
        SupplierProfileView.as_view(),
        name="supplier-profile"
    ),

    # PRODUCT CATEGORIES
    path(
        "suppliers/dashboard/categories/",
        ProductCategoryListView.as_view(),
        name="supplier-categories"
    ),

    # PRODUCTS
    path(
        "suppliers/dashboard/products/",
        ProductListCreateView.as_view(),
        name="supplier-products"
    ),

    # SINGLE PRODUCT
    path(
        "suppliers/dashboard/products/<int:pk>/",
        ProductDetailView.as_view(),
        name="supplier-product-detail"
    ),

    # =====================================
    # BUYER DASHBOARD
    # =====================================

    path(
        "buyers/dashboard/",
        BuyerDashboardView.as_view(),
        name="buyer-dashboard"
    ),
    
    path("health/", HealthCheckView.as_view()),
    
]

