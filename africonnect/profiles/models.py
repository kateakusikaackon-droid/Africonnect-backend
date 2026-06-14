from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class SupplierProfile(models.Model):

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="supplier_profile"
    )
    business_name = models.CharField(max_length=255, blank=True)

    verified = models.BooleanField(default=False)

    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)

    image = models.ImageField(upload_to="profiles/suppliers/", blank=True, null=True)

    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} Supplier_Profile"

    ##OR

    # def __str__(self):
    # return self.name

    ##OR

    # def __str__(self):
    # return self.business_name


class BuyerProfile(models.Model):

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    id = models.AutoField(primary_key=True)

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="buyer_profile"
    )

    business_name = models.CharField(max_length=255, blank=True)

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)

    phone_number = models.CharField(max_length=20, blank=True)

    country = models.CharField(max_length=100, blank=True)

    industry = models.CharField(max_length=255, blank=True)

    company_description = models.TextField(blank=True)

    address = models.TextField(blank=True)

    website = models.URLField(blank=True)

    image = models.ImageField(upload_to="profiles/buyers/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} Buyer_Profile"
