from django.urls import path
from .views import ProductCategoryListView, ProductListCreateView, ProductDetailView

urlpatterns = [
    path("categories/", ProductCategoryListView.as_view(), name="categories"),
    path("", ProductListCreateView.as_view(), name="products"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
]




