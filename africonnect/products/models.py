from django.db import models
from django.conf import settings
from profiles.models import SupplierProfile

User = settings.AUTH_USER_MODEL


class ProductCategory(models.Model):

    name = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    supplier = models.ForeignKey(
        SupplierProfile, on_delete=models.CASCADE, related_name="products"
    )

    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    moq = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, default="USD")
    unit = models.CharField(max_length=20, default="ton")
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.name
