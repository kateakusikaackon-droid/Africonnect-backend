from django.contrib import admin
from .models import SupplierProfile, BuyerProfile


@admin.register(SupplierProfile)
class SupplierProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "business_name", "country", "verified")


@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "business_name", "country")
