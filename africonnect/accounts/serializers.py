from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User

        fields = [
            "id",
            "name",
            "business_name",
            "email",
            "password",
        ]

        read_only_fields = ["id","business_name"]

    # -----------------------------
    # VALIDATION
    # -----------------------------
    def validate_email(self, value):

        value = value.lower()

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")

        return value

    def validate_password(self, value):

        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters"
            )

        return value

    # -----------------------------
    # CREATE USER (ROLE-BASED)
    # -----------------------------
    def create(self, validated_data):

        role = self.context.get("role")

        validated_data["email"] = validated_data["email"].lower()
        validated_data["role"] = role

        return User.objects.create_user(**validated_data)
    
    
    
class CustomTokenSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):

        data = super().validate(attrs)

        data["user"] = {
            "id": self.user.id,
            "name": self.user.name,
            "email": self.user.email,
            "role": self.user.role,
            "business_name": self.user.business_name,
        }

        return data
    
    
    
    
class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField(
        required=True,
        help_text="Refresh token to blacklist"
    )
    




class SupplierDashboardSerializer(
    serializers.Serializer
):

    business_name = (
        serializers.CharField()
    )

    verified = (
        serializers.BooleanField()
    )

    completion_rate = (
        serializers.IntegerField()
    )

    rating = (
        serializers.FloatField()
    )

    products_count = (
        serializers.IntegerField()
    )

    categories_count = (
        serializers.IntegerField()
    )

    verification_steps_completed = (
        serializers.IntegerField()
    )

    verification_total_steps = (
        serializers.IntegerField()
    )    
    
    
    
class BuyerDashboardSerializer(serializers.Serializer):

    message = (
        serializers.CharField()
    )
    
    