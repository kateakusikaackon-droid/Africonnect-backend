# Image Upload Plan (R2) With Code Implementation

## Goal
Make every API endpoint that currently accepts an image field behave as true file upload:
- Upload incoming image files to Cloudflare R2
- Save the object key in ImageField
- Return a frontend-usable absolute URL in API responses (in image)

## 1) Settings: finalize R2 + public media URL
File: africonnect/config/settings.py

Where (exact place):
- In the existing R2 settings block (where AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_ENDPOINT_URL already exist).
- Add R2_PUBLIC_BASE_URL directly after AWS_S3_ENDPOINT_URL.
- Add STORAGES in your storage/static config area.

Why this change:
- Ensures uploaded media is stored in R2.
- Ensures image URLs can be constructed for frontend rendering when there is no custom media domain.

Code:
```python
AWS_ACCESS_KEY_ID = config("R2_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("R2_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config("R2_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = config("R2_ENDPOINT_URL")

# Example: https://pub-xxxxxxxx.r2.dev
R2_PUBLIC_BASE_URL = config("R2_PUBLIC_BASE_URL", default="").rstrip("/")

AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

## 2) Shared image helper fields
File: africonnect/common/serializers.py

Where (exact place):
- Keep CategorySerializer unchanged.
- Add PublicImageUrlField and FileOnlyImageField below CategorySerializer.

Why this change:
- Centralizes image URL output behavior and write validation.
- Prevents repeating image logic in products/profiles/marketplace serializers.

Code:
```python
from urllib.parse import urljoin

from django.conf import settings
from rest_framework import serializers


class PublicImageUrlField(serializers.ImageField):
    """Returns absolute URL for frontend rendering."""

    def to_representation(self, value):
        if not value:
            return None

        try:
            storage_url = value.url
            if storage_url:
                request = self.context.get("request") if hasattr(self, "context") else None
                if request is not None:
                    return request.build_absolute_uri(storage_url)
                return storage_url
        except Exception:
            pass

        object_key = str(value).lstrip("/")
        base = getattr(settings, "R2_PUBLIC_BASE_URL", "")
        if base:
            return urljoin(f"{base}/", object_key)

        return object_key


class FileOnlyImageField(PublicImageUrlField):
    """Rejects plain string payloads on write; requires multipart file upload."""

    def to_internal_value(self, data):
        if isinstance(data, str):
            raise serializers.ValidationError(
                "Image must be uploaded as a file using multipart/form-data."
            )
        return super().to_internal_value(data)
```

## 3) Product serializers: enforce file upload + URL output
File: africonnect/products/serializers.py

Where (exact place):
- Top imports: add from common.serializers import FileOnlyImageField.
- In class ProductSerializer: add image = FileOnlyImageField(required=False, allow_null=True) above class Meta.
- In class ProductDetailSerializer: add image = FileOnlyImageField(required=False, allow_null=True) above class Meta.

Why this change:
- Product create/update should accept actual files, not string placeholders.
- Product response image should always be frontend-usable URL.

Code:
```python
from common.serializers import FileOnlyImageField


class ProductSerializer(serializers.ModelSerializer):
    image = FileOnlyImageField(required=False, allow_null=True)
    ...


class ProductDetailSerializer(serializers.ModelSerializer):
    image = FileOnlyImageField(required=False, allow_null=True)
    ...
```

## 4) Profile serializers: enforce file upload + URL output
File: africonnect/profiles/serializers.py

Where (exact place):
- Top imports: add from common.serializers import FileOnlyImageField.
- In class SupplierProfileSerializer: add image = FileOnlyImageField(required=False, allow_null=True) above class Meta.
- In class BuyerProfileSerializer: add image = FileOnlyImageField(required=False, allow_null=True) above class Meta.

Why this change:
- Profile patch endpoints currently allow string-shaped data for image.
- This forces real file upload behavior and consistent response URLs.

Code:
```python
from common.serializers import FileOnlyImageField


class SupplierProfileSerializer(serializers.ModelSerializer):
    image = FileOnlyImageField(required=False, allow_null=True)
    ...


class BuyerProfileSerializer(serializers.ModelSerializer):
    image = FileOnlyImageField(required=False, allow_null=True)
    ...
```

## 5) Marketplace serializers: guarantee URL output
File: africonnect/marketplace/serializers.py

Where (exact place):
- Top imports: add from common.serializers import PublicImageUrlField.
- Add image = PublicImageUrlField(read_only=True) above class Meta in:
  - MarketplaceSupplierSerializer
  - MarketplaceProductSerializer
  - MarketplaceSupplierDetailSerializer
  - MarketplaceProductDetailSerializer

Why this change:
- Marketplace endpoints are consumed directly by frontend listing/detail pages.
- They must always return renderable image URLs.

Code:
```python
from common.serializers import PublicImageUrlField


class MarketplaceSupplierSerializer(serializers.ModelSerializer):
    image = PublicImageUrlField(read_only=True)
    ...


class MarketplaceProductSerializer(serializers.ModelSerializer):
    image = PublicImageUrlField(read_only=True)
    ...


class MarketplaceSupplierDetailSerializer(serializers.ModelSerializer):
    image = PublicImageUrlField(read_only=True)
    ...


class MarketplaceProductDetailSerializer(serializers.ModelSerializer):
    image = PublicImageUrlField(read_only=True)
    ...
```

## 6) Product views: enable multipart parsing
File: africonnect/products/views.py

Where (exact place):
- Top imports: add from rest_framework.parsers import MultiPartParser, FormParser.
- In class ProductListCreateView body: add parser_classes = [MultiPartParser, FormParser].
- In class ProductDetailView body: add parser_classes = [MultiPartParser, FormParser].

Why this change:
- Without multipart parsers, DRF treats image as text in JSON body.
- File upload requires multipart/form-data parsing.

Code:
```python
from rest_framework.parsers import MultiPartParser, FormParser


class ProductListCreateView(SwaggerSafeMixin, ListCreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    ...


class ProductDetailView(SwaggerSafeMixin, RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser, FormParser]
    ...
```

## 7) Profile views: enable multipart parsing
File: africonnect/profiles/views.py

Where (exact place):
- Top imports: add from rest_framework.parsers import MultiPartParser, FormParser.
- In class SupplierProfileView body: add parser_classes = [MultiPartParser, FormParser].
- In class BuyerProfileView body: add parser_classes = [MultiPartParser, FormParser].

Why this change:
- Supplier and buyer profile update endpoints need to parse file uploads.

Code:
```python
from rest_framework.parsers import MultiPartParser, FormParser


class SupplierProfileView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    ...


class BuyerProfileView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    ...
```

## 8) API docs: indicate multipart request
Files:
- africonnect/products/views.py
- africonnect/profiles/views.py

Where (exact place):
- On create/patch methods that accept image upload, add or refine @extend_schema examples.

Why this change:
- Makes integration expectations explicit for frontend and QA.

Code (example pattern):
```python
from drf_spectacular.utils import extend_schema, OpenApiExample


@extend_schema(
    request=ProductDetailSerializer,
    examples=[
        OpenApiExample(
            "Multipart upload",
            description="Send as multipart/form-data; image must be a file.",
            value={"name": "Cassava", "price": "10.00", "image": "<binary file>"},
            request_only=True,
        )
    ],
)
def patch(self, request, *args, **kwargs):
    ...
```

## 9) Tests
Files:
- africonnect/products/tests.py
- africonnect/profiles/tests.py

Where (exact place):
- Add multipart success tests near existing create/update tests.
- Add string-image rejection tests near validation tests.

Why this change:
- Verifies both happy path (file upload works) and guardrail path (string input rejected).

Code examples:
```python
from django.core.files.uploadedfile import SimpleUploadedFile


def test_product_create_with_image_multipart(api_client, supplier_user):
    api_client.force_authenticate(user=supplier_user)
    image = SimpleUploadedFile("sample.jpg", b"filecontent", content_type="image/jpeg")

    payload = {
        "name": "Rice",
        "price": "12.50",
        "currency": "USD",
        "unit": "kg",
        "moq": 10,
        "country": "NG",
        "category_id": 1,
        "image": image,
    }

    response = api_client.post("/products/", payload, format="multipart")

    assert response.status_code == 201
    assert response.data["image"]
    assert response.data["image"].startswith("http")
```

```python
def test_profile_patch_rejects_image_string(api_client, supplier_user):
    api_client.force_authenticate(user=supplier_user)
    response = api_client.patch(
        "/profiles/supplier/",
        {"image": "https://example.com/not-uploaded.jpg"},
        format="json",
    )

    assert response.status_code == 400
    assert "image" in response.data
```

## 10) Environment and rollout

Where (exact place):
- In deployment environment variables (same place as SECRET_KEY, DATABASE_URL).

Why this change:
- Missing R2 vars or private bucket permissions will break frontend rendering even if upload succeeds.

Required env vars:
```bash
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET_NAME=...
R2_ENDPOINT_URL=...
R2_PUBLIC_BASE_URL=https://pub-xxxxxxxx.r2.dev
```

Recommended rollout order:
1. settings.py
2. common serializer helper fields
3. product/profile/marketplace serializers
4. parser_classes in product/profile views
5. schema examples
6. tests
7. manual verification

Manual verification checklist:
1. POST product with multipart/form-data and a real image file.
2. PATCH supplier profile with multipart/form-data and image file.
3. PATCH buyer profile with multipart/form-data and image file.
4. GET marketplace/product/profile endpoints and confirm image is full URL.
5. Open one returned URL in browser and confirm image loads.

Client contract after change:
- Write image: multipart/form-data file only
- Read image: full URL string

Compatibility note:
- This is intentionally backward-incompatible for clients sending image as plain JSON string.

## 11) Fixes Applied — Implementation Audit Results

These are the exact corrections that were made to the repo. All fixes are now live.

### Fix A: Storage variable names ✅ Applied
File: africonnect/config/settings.py

Issue: Original keys were R2_STORAGE_BUCKET_NAME, R2_S3_ENDPOINT_URL, R2_DEFAULT_ACL, R2_QUERYSTRING_AUTH.
S3Storage requires the AWS_* prefix — wrong names caused the backend to silently ignore all config values.

Applied code (current state of the R2 config block):
```python
AWS_ACCESS_KEY_ID = config("R2_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("R2_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config("R2_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = config("R2_ENDPOINT_URL")

AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False

R2_PUBLIC_BASE_URL = config("R2_PUBLIC_BASE_URL", default="").rstrip("/")

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

---

### Fix B: common/serializers.py — duplicate imports, logic bugs, missing Swagger annotations ✅ Applied
File: africonnect/common/serializers.py

Issues:
- `from rest_framework import serializers` appeared twice.
- `to_representation` had a broken request assignment with no-op if/else blocks and an unreachable fallback `return`.
- drf-spectacular inferred `string` type for both fields because `to_representation` returns a string URL — image fields rendered as plain text inputs in API docs instead of file upload widgets.

Applied code (complete file as it stands now):
```python
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

        try:
            storage_url = value.url
            if storage_url:
                request = self.context.get("request") if hasattr(self, "context") else None
                if request is not None:
                    return request.build_absolute_uri(storage_url)
                return storage_url
        except Exception:
            pass

        object_key = str(value).lstrip("/")
        base = getattr(settings, "R2_PUBLIC_BASE_URL", "")
        if base:
            return urljoin(f"{base}/", object_key)
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
```

What the Swagger annotations do:
- `@extend_schema_field(OpenApiTypes.URI)` — API docs show image as a URL string in GET responses.
- `@extend_schema_field(OpenApiTypes.BINARY)` — API docs show image as a file upload widget (`type: string, format: binary`) in POST/PATCH request bodies.

---

### Fix C: products/views.py — entire file was duplicated ✅ Applied
File: africonnect/products/views.py

Issue: The entire module (all imports + all three view classes) appeared twice in the file. The second copy was an exact repeat starting from a second `from django_filters...` import block.

Applied code (complete file as it stands now):
```python
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser

from accounts.permissions import IsSupplier
from common.pagination import DefaultLimitOffsetPagination
from common.swagger import SwaggerSafeMixin

from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductCategorySerializer, ProductDetailSerializer


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
```

---

### Fix D: profiles/views.py — GET saved data, PATCH missing, BuyerView had no parsers ✅ Applied
File: africonnect/profiles/views.py

Issues:
- `SupplierProfileView.get()` called `serializer.save()` — a GET handler was mutating the database on every read request.
- `SupplierProfileView.patch()` did not exist — supplier profile could not be updated via the API.
- `BuyerProfileView` had no `parser_classes` — file uploads would not be parsed.

Applied code (complete file as it stands now):
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema

from accounts.permissions import IsSupplier, IsBuyer
from .models import SupplierProfile, BuyerProfile
from .serializers import SupplierProfileSerializer, BuyerProfileSerializer


class SupplierProfileView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsSupplier]
    serializer_class = SupplierProfileSerializer

    @extend_schema(responses=SupplierProfileSerializer)
    def get(self, request):
        try:
            supplier = request.user.supplier_profile
        except SupplierProfile.DoesNotExist:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(supplier)
        return Response(serializer.data)

    @extend_schema(request=SupplierProfileSerializer, responses=SupplierProfileSerializer)
    def patch(self, request):
        try:
            supplier = request.user.supplier_profile
        except SupplierProfile.DoesNotExist:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(supplier, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BuyerProfileView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsBuyer]
    serializer_class = BuyerProfileSerializer

    @extend_schema(responses=BuyerProfileSerializer)
    def get(self, request):
        try:
            buyer = request.user.buyer_profile
        except BuyerProfile.DoesNotExist:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(buyer)
        return Response(serializer.data)

    @extend_schema(request=BuyerProfileSerializer, responses=BuyerProfileSerializer)
    def patch(self, request):
        try:
            buyer = request.user.buyer_profile
        except BuyerProfile.DoesNotExist:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(buyer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
```

---

### Fix E: marketplace/serializers.py — duplicated classes, wrong image field type ✅ Applied
File: africonnect/marketplace/serializers.py

Issues:
- All serializer classes (MarketplaceSupplierSerializer, MarketplaceProductSerializer, MarketplaceSupplierDetailSerializer, MarketplaceProductDetailSerializer, MarketplaceCategorySerializer) were defined twice in the same file. The second definitions silently overrode the first.
- All image fields used `FileOnlyImageField` — a write-only field that rejects string input. Marketplace endpoints are read-only listing/detail views; they do not accept uploads. Using a write field here caused serialization errors on GET responses.

Applied code (complete file as it stands now):
```python
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from profiles.models import SupplierProfile
from products.models import Product, ProductCategory

from common.serializers import PublicImageUrlField


class MarketplaceSupplierSerializer(serializers.ModelSerializer):
    image = PublicImageUrlField(read_only=True)

    class Meta:
        model = SupplierProfile
        fields = ["id", "business_name", "rating", "verified", "completion_rate", "country", "image"]


class MarketplaceProductSerializer(serializers.ModelSerializer):
    image = PublicImageUrlField(read_only=True)
    supplier = MarketplaceSupplierSerializer(read_only=True)
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ["id", "name", "price", "moq", "country", "image", "supplier", "category"]


class MarketplaceSupplierDetailSerializer(serializers.ModelSerializer):
    image = PublicImageUrlField(read_only=True)
    products = serializers.SerializerMethodField()

    class Meta:
        model = SupplierProfile
        fields = [
            "id", "business_name", "rating", "verified", "completion_rate",
            "phone_number", "country", "address", "website", "image", "products",
        ]

    @extend_schema_field(MarketplaceProductSerializer(many=True))
    def get_products(self, obj):
        products = Product.objects.filter(supplier=obj, is_public=True)[:6]
        return MarketplaceProductSerializer(products, many=True, context=self.context).data


class MarketplaceProductDetailSerializer(serializers.ModelSerializer):
    image = PublicImageUrlField(read_only=True)
    related_products = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "description", "price", "moq", "country",
            "image", "category", "supplier", "created_at", "related_products",
        ]

    @extend_schema_field(MarketplaceProductSerializer(many=True))
    def get_related_products(self, obj):
        related = Product.objects.filter(category=obj.category, is_public=True).exclude(id=obj.id)[:6]
        return MarketplaceProductSerializer(related, many=True, context=self.context).data


class MarketplaceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "name"]


class CountryListSerializer(serializers.Serializer):
    countries = serializers.ListField(child=serializers.CharField())
```

---

### Fix F: Validate after all changes

Run after all fixes:
```bash
python manage.py check
python manage.py test
```

Expected: system check passes with no errors; tests confirm upload and rejection behavior.
