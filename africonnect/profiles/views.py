from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from accounts.permissions import IsSupplier
from .models import SupplierProfile
from .serializers import SupplierProfileSerializer


class SupplierProfileView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsSupplier
    ]

    serializer_class = SupplierProfileSerializer

    @extend_schema(
        responses=SupplierProfileSerializer
    )
    def get(self, request):

        try:
            supplier = request.user.supplier_profile

        except SupplierProfile.DoesNotExist:

            return Response(
                {
                    "detail": "Profile not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(
            supplier
        )

        return Response(serializer.data)

    @extend_schema(
        request=SupplierProfileSerializer,
        responses=SupplierProfileSerializer
    )
    def patch(self, request):

        try:
            supplier = request.user.supplier_profile

        except SupplierProfile.DoesNotExist:

            return Response(
                {
                    "detail": "Profile not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(
            supplier,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(serializer.data)