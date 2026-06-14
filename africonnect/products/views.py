from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema

from accounts.permissions import IsSupplier
from common.pagination import DefaultLimitOffsetPagination
from common.swagger import SwaggerSafeMixin

from .models import Product, ProductCategory
from .serializers import (
    ProductSerializer,
    ProductCategorySerializer,
    ProductDetailSerializer,
)


class ProductCategoryListView(ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [AllowAny]


class ProductListCreateView(SwaggerSafeMixin, ListCreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSupplier]
    pagination_class = DefaultLimitOffsetPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "is_public"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "price", "name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        if self.is_swagger():
            return Product.objects.none()

        supplier = self.safe_supplier()
        if not supplier:
            return Product.objects.none()

        return Product.objects.filter(supplier=supplier).select_related("category")

    @extend_schema(request={"multipart/form-data": ProductSerializer}, responses=ProductSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        if self.is_swagger():
            return

        supplier = self.safe_supplier()
        if not supplier:
            return

        serializer.save(supplier=supplier)


class ProductDetailView(SwaggerSafeMixin, RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAuthenticated, IsSupplier]

    def get_queryset(self):
        if self.is_swagger():
            return Product.objects.none()

        supplier = self.safe_supplier()
        if not supplier:
            return Product.objects.none()

        return Product.objects.filter(supplier=supplier).select_related("category")
