from rest_framework import serializers

from profiles.models import SupplierProfile
from products.models import Product, ProductCategory
from drf_spectacular.utils import extend_schema_field
from .services import get_related_products
#from products.serializers import ProductSerializer



from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from profiles.models import SupplierProfile
from products.models import Product, ProductCategory


# =====================================================
# SUPPLIER SERIALIZER (USED INSIDE PRODUCT SERIALIZER)
# =====================================================

class MarketplaceSupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplierProfile

        fields = [
            "id",
            "business_name",
            "rating",
            "verified",
            "completion_rate",
            "country",
            "image",
        ]


# =====================================================
# PRODUCT LIST SERIALIZER (MARKETPLACE CARDS)
# =====================================================

class MarketplaceProductSerializer(serializers.ModelSerializer):

    supplier = MarketplaceSupplierSerializer(read_only=True)
    category = serializers.StringRelatedField()

    class Meta:
        model = Product

        fields = [
            "id",
            "name",
            "price",
            "moq",
            "country",
            "image",
            "supplier",
            "category",
        ]


# =====================================================
# SUPPLIER DETAIL SERIALIZER (WITH PRODUCTS)
# =====================================================

class MarketplaceSupplierDetailSerializer(serializers.ModelSerializer):

    products = serializers.SerializerMethodField()

    class Meta:
        model = SupplierProfile

        fields = [
            "id",
            "business_name",
            "rating",
            "verified",
            "completion_rate",
            "phone_number",
            "country",
            "address",
            "website",
            "image",
            "products",
        ]

    @extend_schema_field(MarketplaceProductSerializer(many=True))
    def get_products(self, obj):

        products = Product.objects.filter(
            supplier=obj,
            is_public=True
        )[:6]

        return MarketplaceProductSerializer(
            products,
            many=True,
            context=self.context
        ).data


# =====================================================
# PRODUCT DETAIL SERIALIZER
# =====================================================

class MarketplaceProductDetailSerializer(serializers.ModelSerializer):

    related_products = serializers.SerializerMethodField()

    class Meta:
        model = Product

        fields = [
            "id",
            "name",
            "description",
            "price",
            "moq",
            "country",
            "image",
            "category",
            "supplier",
            "created_at",
            "related_products",
        ]

    @extend_schema_field(MarketplaceProductSerializer(many=True))
    def get_related_products(self, obj):

        related = Product.objects.filter(
            category=obj.category,
            is_public=True
        ).exclude(id=obj.id)[:6]

        return MarketplaceProductSerializer(
            related,
            many=True,
            context=self.context
        ).data


# =====================================================
# CATEGORY SERIALIZER
# =====================================================

class MarketplaceCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory

        fields = [
            "id",
            "name",
        ]


# =====================================================
# COUNTRY LIST SERIALIZER
# =====================================================

class CountryListSerializer(serializers.Serializer):
    countries = serializers.ListField(
        child=serializers.CharField()
    )




