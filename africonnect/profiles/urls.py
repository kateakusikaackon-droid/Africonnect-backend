from django.urls import path
from .views import SupplierProfileView
from .views import BuyerProfileView


urlpatterns = [
    path("supplier/", SupplierProfileView.as_view(), name="supplier-profile"),
    path(
        "buyer/",
        BuyerProfileView.as_view(),
        name="buyer-profile"
    ),

]





