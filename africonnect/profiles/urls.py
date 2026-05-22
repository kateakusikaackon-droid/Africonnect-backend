from django.urls import path
from .views import SupplierProfileView

urlpatterns = [
    path("supplier/", SupplierProfileView.as_view(), name="supplier-profile"),
]