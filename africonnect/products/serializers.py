from rest_framework import serializers
from .models import Product, ProductCategory




class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = [
            "id",
            "name",
        ]


# =====================================
# PRODUCT LIST SERIALIZER
# =====================================

class ProductSerializer(serializers.ModelSerializer):

    category = ProductCategorySerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(),
        source="category",
        write_only=True
    )
    
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "currency",
            "unit",
            "moq",
            "country",
            "image",
            "is_public",
            "category",
            "category_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "category_id", "created_at", "updated_at"]



# =====================================
# PRODUCT DETAIL SERIALIZER
# =====================================

class ProductDetailSerializer(serializers.ModelSerializer):

    category = ProductCategorySerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(),
        source="category",
        write_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "currency",
            "unit",
            "moq",
            "country",
            "city",
            "image",
            "is_public",
            "category",
            "category_id",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["id", "created_at", "updated_at"]

        