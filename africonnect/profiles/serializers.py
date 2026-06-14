from rest_framework import serializers
from .models import SupplierProfile
from .models import BuyerProfile
from common.serializers import FileOnlyImageField


class SupplierProfileSerializer(serializers.ModelSerializer):

    supplier_name = serializers.CharField(source="user.name", read_only=True)
    image = FileOnlyImageField(required=False, allow_null=True)

    class Meta:
        model = SupplierProfile
        fields = [
            "id",
            "supplier_name",
            "business_name",
            "rating",
            "verified",
            "completion_rate",
            "phone_number",
            "country",
            "address",
            "website",
            "image",
            "is_public",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class BuyerProfileSerializer(serializers.ModelSerializer):

    buyer_name = serializers.CharField(source="user.name", read_only=True)
    image = FileOnlyImageField(required=False, allow_null=True)

    class Meta:
        model = BuyerProfile
        fields = [
            "id",
            "buyer_name",
            "business_name",
            "phone_number",
            "industry",
            "company_description",
            "address",
            "website",
            "country",
            "image",
        ]
        read_only_fields = ["id"]
