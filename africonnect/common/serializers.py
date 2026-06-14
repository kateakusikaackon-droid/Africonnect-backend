# common/serializers.py

from urllib.parse import urljoin

from django.conf import settings
from rest_framework import serializers
from products.models import ProductCategory
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "name"]


@extend_schema_field(OpenApiTypes.URI)
class PublicImageUrlField(serializers.ImageField):
    """Read-only field: returns an absolute URL string for frontend rendering."""

    def to_representation(self, value):
        if not value:
            return None

        object_key = str(value).lstrip("/")
        base = getattr(settings, "R2_PUBLIC_BASE_URL", "").rstrip("/")
        if base:
            return f"{base}/{object_key}"

        try:
            storage_url = value.url
            if storage_url:
                request = (
                    self.context.get("request") if hasattr(self, "context") else None
                )
                if request is not None:
                    return request.build_absolute_uri(storage_url)
                return storage_url
        except Exception:
            pass

        return object_key


@extend_schema_field(OpenApiTypes.BINARY)
class FileOnlyImageField(PublicImageUrlField):
    """Write field: accepts only file uploads (rejects string placeholders)."""

    def to_internal_value(self, data):
        if isinstance(data, str):
            raise serializers.ValidationError(
                "Image must be uploaded as a file using multipart/form-data."
            )
        return super().to_internal_value(data)
