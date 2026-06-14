from django.urls import path

from .views import (
    MarketplaceProductListView,
    MarketplaceProductDetailView,
    MarketplaceSupplierListView,
    MarketplaceSupplierDetailView,
    MarketplaceCategoryListView,
    CountryListView,
)

urlpatterns = [
    path(
        "products/",
        MarketplaceProductListView.as_view(),
        name="marketplace-products",
    ),
    path(
        "products/<int:id>/",
        MarketplaceProductDetailView.as_view(),
    ),
    path(
        "suppliers/",
        MarketplaceSupplierListView.as_view(),
        name="marketplace-suppliers",
    ),
    path(
        "suppliers/<int:pk>/",
        MarketplaceSupplierDetailView.as_view(),
        name="marketplace-supplier-detail",
    ),
    path(
        "categories/",
        MarketplaceCategoryListView.as_view(),
        name="marketplace-categories",
    ),
    path(
        "countries/",
        CountryListView.as_view(),
        name="marketplace-countries",
    ),
]
