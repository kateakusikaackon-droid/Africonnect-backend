from django.db import models

# Create your models here.

# rfqs/models.py

from django.conf import settings


class RFQ(models.Model):

    UNIT_CHOICES = [
        ("QTY", "Quantity"),
        ("KG", "Kilograms"),
        ("TON", "Tons"),
        ("L", "Litres"),
    ]

    CATEGORY_CHOICES = [
        ("Agriculture & Food Raw Materials", "Agriculture & Food Raw Materials"),
        ("Textile & Fibres", "Textile & Fibres"),
        ("Chemicals & Petrochemicals", "Chemicals & Petrochemicals"),
        ("Minerals, Ores & Metals", "Minerals, Ores & Metals"),
        ("Wood, Pulp & Paper", "Wood, Pulp & Paper"),
        ("Packaging Materials", "Packaging Materials"),
        ("Building & Construction Materials", "Building & Construction Materials"),
    ]

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="buyer_rfqs"
    )

    product_category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    commodity_type = models.CharField(max_length=255)

    quantity_required = models.DecimalField(max_digits=12, decimal_places=2)

    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default="QTY")

    delivery_timeline = models.DateField()

    target_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    specifications = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commodity_type} RFQ"
