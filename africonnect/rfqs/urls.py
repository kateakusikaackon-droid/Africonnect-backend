# rfqs/urls.py

from django.urls import path

from .views import (
    RFQFormConfigView,
    RFQCreateView,
)

urlpatterns = [

    # OPEN RFQ FORM
    path(
        "form/",
        RFQFormConfigView.as_view(),
        name="rfq-form"
    ),

    # SUBMIT RFQ
    path(
        "create/",
        RFQCreateView.as_view(),
        name="submit-rfq"
    ),
]
