from rest_framework import serializers
from .models import SupplierProfile


class SupplierProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplierProfile
        fields = [
            "id",
            "user",
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
        read_only_fields = ["id", "user", "created_at", "updated_at"]
        
        
    