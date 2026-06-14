from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from profiles.models import SupplierProfile
from products.models import Product, ProductCategory

from common.serializers import PublicImageUrlField


class MarketplaceSupplierSerializer(serializers.ModelSerializer):
    image = PublicImageUrlField(read_only=True)

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


class MarketplaceProductSerializer(serializers.ModelSerializer):
    image = PublicImageUrlField(read_only=True)
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


class MarketplaceSupplierDetailSerializer(serializers.ModelSerializer):
    image = PublicImageUrlField(read_only=True)
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
        products = Product.objects.filter(supplier=obj, is_public=True)[:6]
        return MarketplaceProductSerializer(
            products, many=True, context=self.context
        ).data


class MarketplaceProductDetailSerializer(serializers.ModelSerializer):
    image = PublicImageUrlField(read_only=True)
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
        related = Product.objects.filter(category=obj.category, is_public=True).exclude(
            id=obj.id
        )[:6]
        return MarketplaceProductSerializer(
            related, many=True, context=self.context
        ).data


class MarketplaceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "name"]


class CountryListSerializer(serializers.Serializer):
    countries = serializers.ListField(child=serializers.CharField())
