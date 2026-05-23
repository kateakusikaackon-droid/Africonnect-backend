# rfqs/serializers.py

from rest_framework import serializers
from .models import RFQ


class RFQFormConfigSerializer(serializers.Serializer):
    product_categories = serializers.ListField()
    units = serializers.ListField()

class RFQSerializer(serializers.ModelSerializer):

    class Meta:
        model = RFQ

        fields = [
            "id",
            "buyer",
            "product_category",
            "commodity_type",
            "quantity_required",
            "unit",
            "delivery_timeline",
            "target_price",
            "specifications",
            "created_at",
        ]

        read_only_fields = [
            "buyer",
            "created_at",
        ]        