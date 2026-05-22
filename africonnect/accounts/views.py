from .permissions import IsSupplier, IsBuyer

from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)

from common.swagger import SwaggerSafeMixin



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    UserRegisterSerializer,
    CustomTokenSerializer,
    LogoutSerializer,
    SupplierDashboardSerializer,
    BuyerDashboardSerializer
)

from profiles.models import SupplierProfile
from products.models import Product
from products.models import ProductCategory




@extend_schema(
    request=UserRegisterSerializer,
    responses={201: UserRegisterSerializer},
    description="User registration endpoint (supplier or buyer)"
)
class UserRegisterView(APIView):

    permission_classes = [AllowAny]

    serializer_class = UserRegisterSerializer

    @extend_schema(request=UserRegisterSerializer)
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data,
            context={
                "role": kwargs.get("role")  # supplier or buyer
            }
        )

        if serializer.is_valid():

            user = serializer.save()

            return Response(
                {
                    "message": "User registered successfully",
                    "user": {
                        "email": user.email,
                        "name": user.name,
                        "role": user.role,
                        "business_name": user.business_name,
                    }
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginView(TokenObtainPairView):

    serializer_class = CustomTokenSerializer

    @extend_schema(
        request=CustomTokenSerializer,
        responses={200: OpenApiResponse(description="JWT tokens returned")},
        description="Login and return JWT tokens for supplier or buyer"
    )
    def post(self, request, *args, **kwargs):

        response = super().post(request, *args, **kwargs)

        # OPTIONAL ENHANCEMENT: attach user info
        if response.status_code == 200:

            from django.contrib.auth import get_user_model
            User = get_user_model()

            user = User.objects.get(email=request.data.get("email"))

            response.data["user"] = {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "name": user.name
            }

        return response




class LogoutView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            refresh_token = serializer.validated_data["refresh"]

            try:
                token = RefreshToken(refresh_token)
                token.blacklist()

                return Response(
                    {"detail": "Logout successful"},
                    status=status.HTTP_200_OK
                )

            except Exception:
                return Response(
                    {"detail": "Invalid token"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class SupplierDashboardView(
    SwaggerSafeMixin,
    APIView
):
    """
    Here "supplier" is simply the current
    SupplierProfile object belonging to
    the logged-in supplier user.
    """

    permission_classes = [
        IsAuthenticated,
        IsSupplier
    ]

    serializer_class = (
        SupplierDashboardSerializer
    )

    def get(self, request):

        # =====================================
        # SWAGGER SAFE
        # =====================================

        if self.is_swagger():

            return Response(
                {
                    "message": (
                        "Swagger schema generation"
                    ),
                    "data": {}
                },
                status=status.HTTP_200_OK
            )

        # =====================================
        # SAFE SUPPLIER ACCESS
        # =====================================

        supplier = self.safe_supplier()

        if not supplier:

            return Response(
                {
                    "detail": (
                        "Supplier profile not found"
                    )
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # =====================================
        # RELATED DATA
        # =====================================

        products = supplier.products.all()

        categories = (
            ProductCategory.objects.filter(
                products__supplier=supplier
            ).distinct()
        )

        # =====================================
        # VERIFICATION PROGRESS
        # =====================================

        verification_steps_completed = 0

        if supplier.business_name:
            verification_steps_completed += 1

        if products.exists():
            verification_steps_completed += 1

        if supplier.verified:
            verification_steps_completed += 1

        # =====================================
        # DASHBOARD DATA
        # =====================================

        data = {
            "business_name": (
                supplier.business_name
            ),
            "verified": supplier.verified,
            "completion_rate": (
                supplier.completion_rate
            ),
            "rating": supplier.rating,
            "products_count": (
                products.count()
            ),
            "categories_count": (
                categories.count()
            ),
            "verification_steps_completed": (
                verification_steps_completed
            ),
            "verification_total_steps": 3,
        }

        serializer = self.serializer_class(
            instance=data
        )

        return Response(
            {
                "message": (
                    "Dashboard loaded successfully"
                ),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )





class BuyerDashboardView(APIView):

    permission_classes = [IsAuthenticated, IsBuyer]

    serializer_class = BuyerDashboardSerializer

    @extend_schema(responses=BuyerDashboardSerializer)
    def get(self, request):

        data = {
            "message": "Welcome Buyer"}

        serializer = self.serializer_class(
            instance=data
        )

        return Response(
            {
                "message": (
                    "Dashboard loaded successfully"
                ),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )














class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({"status": "ok"})



